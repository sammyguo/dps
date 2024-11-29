from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from pda.models import StockInRecord, StockOutRecord
from pda.serializers import StockInRecordSerializer, StockOutRecordSerializer
from ptl.models import StockInOrder, StockOutOrder


class HomeView(View):
    def get(self, request):
        stockinorders = StockInOrder.objects.all()
        stockoutorders = StockOutOrder.objects.all()

        context = {
            'toptitle': '拣配任务',
            'stockinorders': stockinorders,
            'stockoutorders': stockoutorders,
        }
        return render(request, 'pda/index.html', context)


def stockin(request, pk):
    # 获取入库单号
    in_order = get_object_or_404(StockInOrder, pk=pk)

    # 查询入库单下的所有货物及其相关记录，减少数据库查询次数
    goods = in_order.stockingoods_set.all()
    stock_in_records = StockInRecord.objects.filter(goods_code__in=[good.goods_code for good in goods])

    # 构建货物编码到库位编码的映射
    record_mapping = {record.goods_code: record.location_code for record in stock_in_records}
    good_location = {good.goods_code: record_mapping.get(good.goods_code, "") for good in goods}

    # 渲染模板
    return render(request, 'pda/stock_in.html', {
        'toptitle': f'{in_order.src_order} 拣配',
        'good_location': good_location,
    })


def stockout(request, pk):
    # 获取出库单号
    out_order = get_object_or_404(StockOutOrder, pk=pk)

    # 查询入库单下的所有货物及其相关记录，减少数据库查询次数
    out_goods = out_order.stockoutgoods_set.all()

    stock_in_records = StockInRecord.objects.filter(goods_code__in=[good.goods_code for good in out_goods])

    # 构建货物编码到库位编码的映射
    record_mapping = {record.goods_code: record.location_code for record in stock_in_records}

    good_location = {good.goods_code: record_mapping.get(good.goods_code, "") for good in out_goods}

    # 渲染模板
    return render(request, 'pda/stock_out.html', {
        'toptitle': f'{out_order.src_order} 拣配',
        'good_location': good_location,
    })


class StockInRecordListView(ListView):
    model = StockInRecord
    template_name = 'pda/stock_in_record_list.html'
    context_object_name = 'records'
    extra_context = {
        'menu_title': '入库上架绑定货品库位记录',
    }


class StockOutRecordListView(ListView):
    model = StockOutRecord
    template_name = 'pda/stock_out_record_list.html'
    context_object_name = 'records'
    extra_context = {
        'menu_title': '出库下架货品库位记录',
    }


""" Djangorestframework viewsets """


@method_decorator(csrf_exempt, name='dispatch')
class StockInRecordViewSet(viewsets.ModelViewSet):
    """入库上架绑定货品库位记录"""
    queryset = StockInRecord.objects.all()
    serializer_class = StockInRecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['goods_code', 'location_code']


@method_decorator(csrf_exempt, name='dispatch')
class StockOutRecordViewSet(viewsets.ModelViewSet):
    """入库上架绑定货品库位记录"""
    queryset = StockOutRecord.objects.all()
    serializer_class = StockOutRecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['goods_code', 'location_code']
