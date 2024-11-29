import struct

from django import forms
from django.forms import formset_factory, inlineformset_factory

from .device_protocol import *

from .models import Warehouse, Location, Label, StockInOrder, StockInGoods, StockOutOrder, StockOutGoods


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = '__all__'


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = '__all__'


class StockInOrderForm(forms.ModelForm):
    class Meta:
        model = StockInOrder
        fields = '__all__'

        widgets = {
            'remark': forms.TextInput(attrs={'class': 'col-md-10'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # 如果是新增而非编辑
            self.fields['number'].initial = StockInOrder.get_number()


class StockInGoodsForm(forms.ModelForm):
    class Meta:
        model = StockInGoods
        fields = '__all__'


StockInGoodsFormSet = inlineformset_factory(
    StockInOrder,  # 父模型
    StockInGoods,  # 子模型
    fields='__all__',
    extra=0,  # 默认额外显示一行
    can_delete=True,  # 允许删除

    widgets={
        'goods_code': forms.TextInput(attrs={'class': 'form-control'}),
        'goods_desc': forms.TextInput(attrs={'class': 'form-control'}),
        'plan_qty': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100px;'}),
        'actual_qty': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100px;'}),
        'batch': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 150px;'}),
        'location_code': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 150px;'}),
    }
)


class StockOutOrderForm(forms.ModelForm):
    class Meta:
        model = StockOutOrder
        fields = '__all__'

        widgets = {
            'remark': forms.TextInput(attrs={'class': 'col-md-10'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # 如果是新增而非编辑
            self.fields['number'].initial = StockOutOrder.get_number()


class StockOutGoodsForm(forms.ModelForm):
    class Meta:
        model = StockOutGoods
        fields = '__all__'


StockOutGoodsFormSet = inlineformset_factory(
    StockOutOrder,  # 父模型
    StockOutGoods,  # 子模型
    fields='__all__',
    extra=0,  # 默认额外显示一行
    can_delete=True,  # 允许删除

    widgets={
        'goods_code': forms.TextInput(attrs={'class': 'form-control'}),
        'goods_desc': forms.TextInput(attrs={'class': 'form-control'}),
        'plan_qty': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100px;'}),
        'actual_qty': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100px;'}),
        'batch': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 150px;'}),
        'supplier_batch': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 150px;'}),
        'location_code': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 150px;'}),
    }
)


# 标签控制数据结构
class LabelControlCommand:
    def __init__(self, node_id, color, mode):
        self.node_id = node_id  # 标签ID
        self.color = color  # 颜色
        self.mode = mode  # 模式

    def to_raw_data(self):
        return struct.pack(">H", self.node_id) + struct.pack(">B", self.color) + struct.pack(">B", self.mode)

    def __repr__(self):
        return f"LabelControlCommand(node_id={self.node_id}, color={self.color}, mode={self.mode})"


class LabelControlForm(forms.Form):
    node_id = forms.IntegerField(
        min_value=1,
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': '标签ID/组ID'})
    )
    color = forms.ChoiceField(
        required=False,
        choices=[('', '请选择颜色')] + [(color.name, color.name) for color in T_GUI_COLOR],
    )
    mode = forms.ChoiceField(
        required=False,
        choices=[('', '请选择模式')] + [(mode.name, mode.name) for mode in T_GUI_MODE],
    )


LabelControlFormSet = formset_factory(LabelControlForm, extra=7, can_delete=True)  # 默认显示3个表单
