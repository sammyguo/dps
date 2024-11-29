from enum import IntEnum

from django.http import JsonResponse


# cmd定义
class T_NET_CMD(IntEnum):
    NET_CMD_NONE = 0x0000

    # 对标签的控制
    NET_CMD_LABLE_LIGHT_SET = 0x0010
    NET_CMD_LABLE_INFO_GET = 0x0020
    NET_CMD_LABLE_RST = 0x0030

    # 对控制板的操作
    NET_CMD_CTL_IP_ADDR_SET = 0x0080
    NET_CMD_CTL_IP_ADDR_GET = 0x0081
    NET_CMD_CTL_IP_PORT_SET = 0x0082
    NET_CMD_CTL_IP_PORT_GET = 0x0083
    NET_CMD_CTL_SYS_RST = 0x0084
    NET_CMD_CTL_SYS_DEF = 0x0085

    NET_CMD_NUM = 0xFFFF


CMD_DESCRIPTIONS = {cmd.value: cmd.name for cmd in T_NET_CMD}


# event 定义
class T_NET_EVT(IntEnum):
    NET_EVT_NONE = 0x0000
    NET_EVT_ACK = 0x0001
    NET_EVT_LABLE_INFO = 0x0020
    NET_EVT_CTL_IP_ADDR = 0x0081
    NET_EVT_CTL_IP_PORT = 0x0083
    NET_EVT_NUM = 0xFFFF
EVT_DESCRIPTIONS = {cmd.value: cmd.name for cmd in T_NET_CMD}

# ack 定义：
class T_NET_ACK(IntEnum):
    NET_ACK_SUC = 0x0000
    NET_ACK_ERR_PARA = 0x0001
    NET_ACK_ERR_BUSY = 0x0002
    NET_ACK_NUM = 0xFFFF


# 对于标签的控制，会带有控制的范围定义：
class T_NET_LABLE(IntEnum):
    NET_LABLE_NONE = 0x00
    NET_LABLE_NODE = 0x01  # 对几个标签节点进行控制
    NET_LABLE_SECTION = 0x02  # 对一组标签进行控制，每组250个
    NET_LABLE_TOTAL = 0x03  # 对全部标签进行控制
    NET_LABLE_NUM = 0xFF


# 标签 灯颜色控制
class T_GUI_COLOR(IntEnum):
    GUI_COLOR_NULL = 0x00
    GUI_COLOR_RED = 0x01
    GUI_COLOR_WHITE = 0x02
    GUI_COLOR_YELLOW = 0x03
    GUI_COLOR_GREEN = 0x04
    GUI_COLOR_INDIGO = 0x05
    GUI_COLOR_BLUE = 0x06
    GUI_COLOR_PURPLE = 0x07
    GUI_COLOR_RSV00 = 0x08  # 选粉色  全灭
    GUI_COLOR_RSV01 = 0x09 # 选海幕色  全亮
    GUI_COLOR_NUM = 0xFF
COLOR_DESCRIPTIONS = {cmd.value: cmd.name for cmd in T_GUI_COLOR}


# 标签 灯模式控制
class T_GUI_MODE(IntEnum):
    GUI_MODE_NULL = 0x00
    GUI_MODE_OFF = 0x01
    GUI_MODE_ON = 0x02
    GUI_MODE_FLASH = 0x03
    GUI_MODE_NUM = 0xFF
MODE_DESCRIPTIONS = {cmd.value: cmd.name for cmd in T_GUI_MODE}

# 定义 ACK 的枚举
LABEL_ACK_ENUM = {
    0x00: "LABEL_ACK_NULL",
    0x01: "LABEL_ACK_SYS_RST",
    0x02: "LABEL_ACK_SET_ON",
    0x03: "LABEL_ACK_GET",
    0x04: "LABEL_ACK_SET_OFF",
    0x05: "LABEL_ACK_KEY_PRESS",
    0x06: "LABEL_ACK_TIMEOUT_OFF",
    0xFF: "LABEL_ACK_NUM",
}

# 枚举类的字典
ENUM_CLASSES = {
    'cmd': T_NET_CMD,
    'event': T_NET_EVT,
    'ack': T_NET_ACK,
    'label': T_NET_LABLE,
    'color': T_GUI_COLOR,
    'mode': T_GUI_MODE,
}


def get_options(option_type):
    # 获取对应的枚举类
    enum_class = ENUM_CLASSES.get(option_type)
    return enum_class


def get_cmd_description(cmd):
    """
    根据命令值获取对应的文本描述
    :param cmd: 命令值 (int)
    :return: 文本描述 (str)
    """
    return CMD_DESCRIPTIONS.get(cmd, f"未知命令 (0x{cmd:04X})")
