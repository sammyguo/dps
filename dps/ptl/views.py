# Create your views here.
import struct
import socket
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

from .forms import LabelControlFormSet, StockInOrderForm, StockInGoodsFormSet, StockOutOrderForm, StockOutGoodsFormSet
from .device_protocol import *

# 设备 IP 和端口（假设已知）
DEVICE_IP = '192.168.1.172'
DEVICE_PORT = 5000


# 格式化十六进制字符串
def format_hex_string(data):
    """格式化二进制数据为 16 进制字符串，每字节用 2 个字符表示"""
    return ' '.join(f'{byte:02x}' for byte in data)


# 计算 CRC16 校验
def calc_crc16(buffer):
    """
    Python 模拟 CRC16 的寄存器更新逻辑。
    """
    crc16d = 0x0000  # 初始化 CRC16D 寄存器
    for byte in buffer:
        crc16d = update_crc16(crc16d, byte)  # 模拟硬件寄存器更新
    return (crc16d >> 8) | ((crc16d & 0xFF) << 8)  # 返回小端序结果


def update_crc16(current_crc, new_byte):
    """
    模拟硬件寄存器的更新逻辑，基于标准 CRC16-CCITT 算法。
    """
    polynomial = 0x1021  # CRC16-CCITT 标准多项式
    crc = current_crc
    crc ^= (new_byte << 8)  # 将新字节加入 CRC 计算
    for _ in range(8):  # 每个字节处理 8 位
        if crc & 0x8000:
            crc = (crc << 1) ^ polynomial
        else:
            crc <<= 1
    return crc & 0xFFFF  # 返回 16 位结果


# 构建raw data函数
def generate_raw_data(node_type_request, node_formset, total_color=None, total_mode=None):
    raw_data = b""

    # 获取标签类型
    node_type = getattr(get_options('label'), node_type_request).value
    raw_data += struct.pack('>B', node_type)  # node_type (1 byte)

    # 节点操作或组操作
    if node_type != 3:  # 如果是节点操作或组操作
        for i in range(int(node_formset.data.get('form-TOTAL_FORMS'))):
            node_id = node_formset.data.get(f'form-{i}-node_id')
            color = node_formset.data.get(f'form-{i}-color')
            mode = node_formset.data.get(f'form-{i}-mode')
            if node_id and color and mode:
                node_id = int(node_id)
                color = getattr(get_options('color'), color)
                mode = getattr(get_options('mode'), mode)
                raw_data += struct.pack('>HBBB', node_id, color, mode, 0)  # 0 用来补位
            else:
                continue
    # 全部操作
    else:  # 如果是全部标签操作
        node_id = 0
        color = getattr(get_options('color'), total_color)
        mode = getattr(get_options('mode'), total_mode)
        raw_data += struct.pack('>HBBB', node_id, color, mode, 0)

    return raw_data


def generate_raw_data_only_node_id(node_type_request, node_formset):
    raw_data = b""
    # 获取标签类型
    node_type = getattr(get_options('label'), node_type_request).value
    raw_data += struct.pack('>B', node_type)  # node_type (1 byte)

    if node_type != 3:  # 如果是节点操作或组操作
        for i in range(int(node_formset.data.get('form-TOTAL_FORMS'))):
            node_id = node_formset.data.get(f'form-{i}-node_id')
            if node_id:
                raw_data += struct.pack('>HH', int(node_id), 0)
            else:
                continue
    else:  # 如果是全部标签操作
        raw_data += struct.pack('>Hh', 0, 0)

    return raw_data


# 构建命令包函数
def build_command_packet(seq, cmd_id, raw_data, header=0xAA, tailer=0x55):
    """
       构建命令包。

       参数:
           seq (int): 序列号
           cmd_id (int): 命令 ID
           raw_data (bytes): 原始数据
           header (int): 包头，默认 0xAA
           tailer (int): 包尾，默认 0x55

       返回:
           bytes: 构建的命令包
       """
    # 确保输入数据类型正确
    if not isinstance(raw_data, bytes):
        raise ValueError("raw_data 必须是 bytes 类型")

    # 计算命令长度 (cmd_len)
    cmd_len = 2 + len(raw_data)  # cmd(2字节) + raw_data 的长度

    # 打包头部信息（header, seq, cmd_len, cmd_id）
    header_packet = struct.pack('>BHHH', header, seq, cmd_len, cmd_id)

    # 组合完整包（不含尾部）
    packet_without_tail = header_packet + raw_data

    # 计算 CRC16 校验值
    crc = calc_crc16(packet_without_tail[1:])  # 从 seq 开始计算

    # 添加 CRC16 和尾部
    final_packet = packet_without_tail + struct.pack('>H', crc) + struct.pack('>B', tailer)

    return final_packet


# 标签控制
def label_control(request):
    node_formset = LabelControlFormSet()
    context = {'node_formset': node_formset}

    return render(request, 'ptl/index.html', context)


# 解析标签回复信息
def parse_label_response(packet):
    """
    解析标签回复信息
    :param packet: bytes 类型的原始数据包
    :return: 解析后的字典信息
    """
    try:
        # 校验数据包最小长度
        if len(packet) < 16:  # Header (1) + seq (2) + len (2) + cmd (2) + raw_data (9) + crc (2) + tailer (1)
            raise ValueError("数据包长度不足！")

        # 校验头和尾
        header, tailer = packet[0], packet[-1]

        # 解析序列号、长度和命令
        seq, length, cmd = struct.unpack_from(">HHH", packet, 1)

        print(f"seq: {seq}, length: {length}, cmd: {cmd}")

        # 校验长度是否匹配
        expected_length = 1 + 2 + 2 + 2 + length + 2 + 1  # header + seq + length + cmd + raw_data + crc + tailer

        if len(packet) != expected_length:
            raise ValueError(f"数据包长度与 length 字段不匹配，期望长度 {expected_length}，实际长度 {len(packet)}！")

        # 提取可变长度的 raw_data 和 CRC
        raw_data_length = length  # `length` 表示 raw_data 的长度
        raw_data_format = f">{raw_data_length}sH"  # 动态构造解包格式
        raw_data, crc = struct.unpack_from(raw_data_format, packet, 7)  # 从第7字节开始解包

        # 解析 raw_data
        # node_id, color, mode, label_ack, battery_voltage, rsv = struct.unpack(">HBBBH2s", raw_data)
        # rsv = int.from_bytes(rsv, byteorder="big")

        # 解析 raw_data 的具体字段（根据你的协议定义解析）
        node_id, color, mode, label_ack, battery_voltage = struct.unpack_from(">HBBBH", raw_data[:7])
        reserved = int.from_bytes(raw_data[7:], byteorder="big") if len(raw_data) > 7 else 0

        # 格式化解析后的数据
        parsed_data = {
            "header": hex(header),
            "seq": hex(seq),
            "length": hex(length),
            "cmd": CMD_DESCRIPTIONS.get(cmd, f"未知命令 ({cmd})"),
            "node_id": node_id,
            "color": COLOR_DESCRIPTIONS.get(color, f"未知颜色 ({color})"),
            "mode": MODE_DESCRIPTIONS.get(mode, f"未知模式 ({mode})"),
            "label_ack": LABEL_ACK_ENUM.get(label_ack, f"未知类型 ({label_ack})"),
            "battery_voltage": f"{battery_voltage / 100}v",
            "reserved": reserved,
            "crc": hex(crc),
            "tailer": hex(tailer),
        }

        return parsed_data

    except Exception as e:
        return {"error": str(e)}


# 配置IP ADDR
def ip_addr_set(request):
    if request.method == 'GET':
        seq = 0  # 序列号，累加
        cmd_id = get_options('cmd').NET_CMD_CTL_IP_ADDR_SET.value  # 标签控制命令
        raw_data = b""

        ip_addr = request.GET.get('ip_addr')  # "192.168.1.172"
        for num in ip_addr.split('.'):
            raw_data += struct.pack('>B', int(num))
        raw_data += struct.pack('>B', 0)  # 填充rsv字节

        packet = build_command_packet(seq, cmd_id, raw_data)

        # 发送命令包到设备
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(packet, (DEVICE_IP, DEVICE_PORT))

        # 返回响应
        context = {'status': 'NET_CMD_CTL_IP_ADDR_SET command sent',
                   'packet': format_hex_string(packet)}

        return JsonResponse(context)  # 返回 JSON 数据
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


# 配置IP 端口
def ip_port_set(request):
    if request.method == 'GET':
        seq = 0  # 序列号，累加
        cmd_id = get_options('cmd').NET_CMD_CTL_IP_PORT_SET.value  # 标签控制命令
        raw_data = b""

        port = request.GET.get('ip_port')
        raw_data += struct.pack('>H', int(port))
        raw_data += struct.pack('>HB', 0, 0)  # 填充rsv字节

        packet = build_command_packet(seq, cmd_id, raw_data)

        # 发送命令包到设备
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(packet, (DEVICE_IP, DEVICE_PORT))

        # 返回响应
        context = {'status': 'NET_CMD_CTL_IP_PORT_SET command sent',
                   'packet': format_hex_string(packet)}

        return JsonResponse(context)  # 返回 JSON 数据
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


# 获取IP地址
def ip_addr_get(request):
    if request.method == 'GET':
        seq = 0  # 序列号，累加
        cmd_id = get_options('cmd').NET_CMD_CTL_IP_ADDR_GET.value
        raw_data = b""

        raw_data += struct.pack('>HHB', 0, 0, 0)  # 填充rsv字节

        packet = build_command_packet(seq, cmd_id, raw_data)

        # 发送命令包到设备
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(packet, (DEVICE_IP, DEVICE_PORT))

        # 返回响应
        context = {'status': 'NET_CMD_CTL_IP_ADDR_GET command sent',
                   'packet': format_hex_string(packet)}

        return JsonResponse(context)  # 返回 JSON 数据
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


# 获取端口号
def ip_port_get(request):
    if request.method == 'GET':
        seq = 0  # 序列号，累加
        cmd_id = get_options('cmd').NET_CMD_CTL_IP_PORT_GET.value
        raw_data = b""

        raw_data += struct.pack('>HHB', 0, 0, 0)  # 填充rsv字节

        packet = build_command_packet(seq, cmd_id, raw_data)

        # 发送命令包到设备
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(packet, (DEVICE_IP, DEVICE_PORT))

        # 返回响应
        context = {'status': 'NET_CMD_CTL_IP_PORT_GET command sent',
                   'packet': format_hex_string(packet)}

        return JsonResponse(context)  # 返回 JSON 数据
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


# 配置IP 系统复位
def sys_rst(request):
    if request.method == 'GET':
        seq = 0  # 序列号，累加
        cmd_id = get_options('cmd').NET_CMD_CTL_SYS_RST.value
        raw_data = b""

        raw_data += struct.pack('>HHB', 0, 0, 0)  # 填充rsv字节

        packet = build_command_packet(seq, cmd_id, raw_data)

        # 发送命令包到设备
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(packet, (DEVICE_IP, DEVICE_PORT))

        # 返回响应
        context = {'status': 'NET_CMD_CTL_SYS_RST command sent',
                   'packet': format_hex_string(packet)}

        return JsonResponse(context)  # 返回 JSON 数据
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


# 配置IP 恢复默认值
def sys_default_set(request):
    if request.method == 'GET':
        seq = 0  # 序列号，累加
        cmd_id = get_options('cmd').NET_CMD_CTL_SYS_DEF.value
        raw_data = b""

        raw_data += struct.pack('>HHB', 0, 0, 0)  # 填充rsv字节

        packet = build_command_packet(seq, cmd_id, raw_data)

        # 发送命令包到设备
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(packet, (DEVICE_IP, DEVICE_PORT))

        # 返回响应
        context = {'status': 'NET_CMD_CTL_SYS_DEF command sent',
                   'packet': format_hex_string(packet)}

        return JsonResponse(context)  # 返回 JSON 数据
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Warehouse, Location, Label, StockInOrder, StockOutOrder
from .forms import WarehouseForm, LocationForm, LabelForm


class WarehouseListView(ListView):
    model = Warehouse
    template_name = 'ptl/warehouse_list.html'
    context_object_name = 'warehouses'
    extra_context = {"menu_title": "仓库的管理"}


class WarehouseCreateView(CreateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'ptl/warehouse_form.html'
    success_url = reverse_lazy('ptl:warehouse_list')
    extra_context = {"menu_title": "新增仓库"}


class WarehouseUpdateView(UpdateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'ptl/warehouse_form.html'
    success_url = reverse_lazy('ptl:warehouse_list')
    extra_context = {"menu_title": "编辑仓库"}


class WarehouseDeleteView(DeleteView):
    model = Warehouse
    success_url = reverse_lazy('ptl:warehouse_list')


class LocationListView(ListView):
    model = Location
    template_name = 'ptl/location_list.html'
    context_object_name = 'locations'
    extra_context = {"menu_title": "库位管理"}


class LocationCreateView(CreateView):
    model = Location
    form_class = LocationForm
    extra_context = {"menu_title": "新增库位"}
    template_name = 'ptl/location_form.html'
    success_url = reverse_lazy('ptl:location_list')


class LocationUpdateView(UpdateView):
    model = Location
    form_class = LocationForm
    template_name = 'ptl/location_form.html'
    success_url = reverse_lazy('ptl:location_list')
    extra_context = {"menu_title": "编辑库位"}


class LocationDeleteView(DeleteView):
    model = Location
    # template_name = 'location_confirm_delete.html'
    success_url = reverse_lazy('ptl:location_list')


class LabelListView(ListView):
    model = Label
    template_name = 'ptl/label_list.html'
    context_object_name = 'labels'
    extra_context = {"menu_title": "标签管理"}


class LabelCreateView(CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'ptl/label_form.html'
    success_url = reverse_lazy('ptl:label_list')
    extra_context = {"menu_title": "新增标签"}


class LabelUpdateView(UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'ptl/label_form.html'
    success_url = reverse_lazy('ptl:label_list')
    extra_context = {"menu_title": "编辑标签"}


class LabelDeleteView(DeleteView):
    model = Label
    # template_name = 'ptl/label_confirm_delete.html'
    success_url = reverse_lazy('ptl:label_list')


class StockInOrderListView(ListView):
    model = StockInOrder
    template_name = 'ptl/stock_in_order_list.html'
    context_object_name = 'stockinorders'
    extra_context = {"menu_title": "入库任务工单管理"}


class StockInOrderCreateView(View):
    def get(self, request):
        order_form = StockInOrderForm()
        goods_formset = StockInGoodsFormSet()
        return render(request, 'ptl/stock_in_order_form.html', {
            'menu_title': '新建入库任务工单',
            'order_form': order_form,
            'goods_formset': goods_formset
        })

    def post(self, request):
        order_form = StockInOrderForm(request.POST)
        goods_formset = StockInGoodsFormSet(request.POST)

        if order_form.is_valid() and goods_formset.is_valid():
            stock_in_order = order_form.save()  # 保存父模型
            goods_instances = goods_formset.save(commit=False)
            for goods in goods_instances:
                goods.stock_in_order = stock_in_order  # 关联父模型
                goods.save()
            return redirect('ptl:stock_in_order_list')  # 跳转到列表页

        return render(request, 'ptl/stock_in_order_form.html', {
            'menu_title': '编辑入库任务工单',
            'order_form': order_form,
            'goods_formset': goods_formset
        })


class StockInOrderUpdateView(View):
    def get(self, request, pk):
        # 获取要编辑的对象
        stock_in_order = get_object_or_404(StockInOrder, pk=pk)
        order_form = StockInOrderForm(instance=stock_in_order)
        goods_formset = StockInGoodsFormSet(instance=stock_in_order)  # 关联表单集
        return render(request, 'ptl/stock_in_order_form.html', {
            'menu_title': '编辑入库任务工单',
            'order_form': order_form,
            'goods_formset': goods_formset,
        })

    def post(self, request, pk):
        stock_in_order = get_object_or_404(StockInOrder, pk=pk)
        order_form = StockInOrderForm(request.POST, instance=stock_in_order)
        goods_formset = StockInGoodsFormSet(request.POST, instance=stock_in_order)

        print(order_form.errors, goods_formset.errors)

        if order_form.is_valid() and goods_formset.is_valid():
            stock_in_order = order_form.save()  # 更新父模型
            goods_instances = goods_formset.save(commit=False)
            for goods in goods_instances:
                goods.stock_in_order = stock_in_order  # 确保子模型关联正确
                goods.save()

            # 删除用户删除的子对象
            goods_formset.deleted_objects and [
                goods.delete() for goods in goods_formset.deleted_objects
            ]

            return redirect('ptl:stock_in_order_list')  # 跳转到列表页

        return render(request, 'ptl/stock_in_order_form.html', {
            'menu_title': '编辑入库任务工单',
            'order_form': order_form,
            'goods_formset': goods_formset,
        })


class StockInOrderDeleteView(DeleteView):
    model = StockInOrder
    # template_name = 'location_confirm_delete.html'
    success_url = reverse_lazy('ptl:stock_in_order_list')


class StockOutOrderListView(ListView):
    model = StockOutOrder
    template_name = 'ptl/stock_out_order_list.html'
    context_object_name = 'stockoutorders'
    extra_context = {"menu_title": "出库任务工单管理"}


class StockOutOrderCreateView(View):
    def get(self, request):
        order_form = StockOutOrderForm()
        goods_formset = StockOutGoodsFormSet()
        return render(request, 'ptl/stock_out_order_form.html', {
            'menu_title': '新建出库任务工单',
            'order_form': order_form,
            'goods_formset': goods_formset
        })

    def post(self, request):
        order_form = StockOutOrderForm(request.POST)
        goods_formset = StockOutGoodsFormSet(request.POST)

        if order_form.is_valid() and goods_formset.is_valid():
            stock_out_order = order_form.save()  # 保存父模型
            goods_outstances = goods_formset.save(commit=False)
            for goods in goods_outstances:
                goods.stock_out_order = stock_out_order  # 关联父模型
                goods.save()
            return redirect('ptl:stock_out_order_list')  # 跳转到列表页

        return render(request, 'ptl/stock_out_order_form.html', {
            'menu_title': '编辑出库任务工单',
            'order_form': order_form,
            'goods_formset': goods_formset
        })


class StockOutOrderUpdateView(View):
    def get(self, request, pk):
        # 获取要编辑的对象
        stock_out_order = get_object_or_404(StockOutOrder, pk=pk)
        order_form = StockOutOrderForm(instance=stock_out_order)
        goods_formset = StockOutGoodsFormSet(instance=stock_out_order)  # 关联表单集
        return render(request, 'ptl/stock_out_order_form.html', {
            'menu_title': '编辑出库任务工单',
            'order_form': order_form,
            'goods_formset': goods_formset,
        })

    def post(self, request, pk):
        stock_out_order = get_object_or_404(StockOutOrder, pk=pk)
        order_form = StockOutOrderForm(request.POST, instance=stock_out_order)
        goods_formset = StockOutGoodsFormSet(request.POST, instance=stock_out_order)

        print(order_form.errors, goods_formset.errors)

        if order_form.is_valid() and goods_formset.is_valid():
            stock_out_order = order_form.save()  # 更新父模型
            goods_outstances = goods_formset.save(commit=False)
            for goods in goods_outstances:
                goods.stock_out_order = stock_out_order  # 确保子模型关联正确
                goods.save()

            # 删除用户删除的子对象
            goods_formset.deleted_objects and [
                goods.delete() for goods in goods_formset.deleted_objects
            ]

            return redirect('ptl:stock_out_order_list')  # 跳转到列表页

        return render(request, 'ptl/stock_out_order_form.html', {
            'menu_title': '编辑出库任务工单',
            'order_form': order_form,
            'goods_formset': goods_formset,
        })


class StockOutOrderDeleteView(DeleteView):
    model = StockOutOrder
    # template_name = 'location_confirm_delete.html'
    success_url = reverse_lazy('ptl:stock_out_order_list')


def label_light_test(request):
    if request.method == 'GET':
        labels = Label.objects.all()
        context = {'labels': labels, 'menu_title': '标签测试'}
    return render(request, 'ptl/label_light_test.html', context)


def single_label_light_test(request, label_id, cmd, mode):
    if request.method == 'GET':
        cmd_id = T_NET_CMD[cmd].value
        color_id = T_GUI_COLOR['GUI_COLOR_WHITE'].value
        mode_id = T_GUI_MODE[mode].value
        seq = 1
        node_type = T_NET_LABLE['NET_LABLE_NODE'].value

        raw_data = b""
        if cmd_id == 16:  # NET_CMD_LABLE_LIGHT_SET
            raw_data += struct.pack('>BHBBB', node_type, label_id, color_id, mode_id, 0)
        elif cmd_id == 32:  # NET_CMD_LABLE_INFO_GET
            raw_data += struct.pack('>BHHB', node_type, label_id, 0, 0)
        else:  # NET_CMD_LABLE_RST
            raw_data += struct.pack('>BHHB', node_type, label_id, 0, 0)

        # 调用 build_command_packet 方法
        packet = build_command_packet(seq, cmd_id, raw_data)

        # 发送命令包到设备
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(packet, (DEVICE_IP, DEVICE_PORT))

        # 返回响应
        context = {'status': 'light set command sent',
                   'packet': f'发送命令: \b {format_hex_string(packet)}'}
        return JsonResponse(context)  # 返回 JSON 数据
    else:
        return redirect('ptl:label_light_test')


def group_label_light_test(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        ids = data.get('ids', [])

        cmd_id = T_NET_CMD[data.get('cmd')].value
        color_id = T_GUI_COLOR[data.get('color')].value
        mode_id = T_GUI_MODE[data.get('mode')].value

        seq = 1
        node_type = T_NET_LABLE['NET_LABLE_NODE'].value

        raw_data = b""
        raw_data += struct.pack('>B', node_type)

        if cmd_id == 16:  # NET_CMD_LABLE_LIGHT_SET
            for label_id in ids:
                raw_data += struct.pack('>HBBB', int(label_id), color_id, mode_id, 0)
        elif cmd_id == 32:  # NET_CMD_LABLE_INFO_GET
            for label_id in ids:
                raw_data += struct.pack('>HHB', int(label_id), 0, 0)
        else:  # NET_CMD_LABLE_RST
            for label_id in ids:
                raw_data += struct.pack('>HHB', int(label_id), 0, 0)

        # 调用 build_command_packet 方法
        packet = build_command_packet(seq, cmd_id, raw_data)
        print(f'发送命令: \b {format_hex_string(packet)}')

        # 发送命令包到设备
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(packet, (DEVICE_IP, DEVICE_PORT))

        # 返回 JSON 响应
        return JsonResponse({'success': True, 'message': '命令已发送'})
    else:
        return JsonResponse({'success': False, 'message': '无效的请求方法'})

