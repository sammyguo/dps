from rest_framework import serializers
from .models import StockInRecord, StockOutRecord


class StockInRecordSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)  # 自定义时间格式

    class Meta:
        model = StockInRecord
        fields = ['id', 'goods_code', 'location_code','create_time']  # 可以根据需要调整字段


class StockOutRecordSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)  # 自定义时间格式

    class Meta:
        model = StockOutRecord
        fields = ['id', 'goods_code', 'location_code','create_time']  # 可以根据需要调整字段