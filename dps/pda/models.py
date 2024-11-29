from django.db import models


# Create your models here.
class StockInRecord(models.Model):
    goods_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='货物编码')
    location_code = models.CharField(max_length=32, blank=True, null=True, verbose_name='库位编号')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '上架绑定货品库位记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.goods_code}-{self.location_code}'


class StockOutRecord(models.Model):
    goods_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='货物编码')
    location_code = models.CharField(max_length=32, blank=True, null=True, verbose_name='库位编号')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '出库下架记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.goods_code}-{self.location_code}'