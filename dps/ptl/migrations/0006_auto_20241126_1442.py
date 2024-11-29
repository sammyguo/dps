# Generated by Django 3.2.16 on 2024-11-26 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ptl', '0005_stockinorder_warehouse_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockoutorder',
            name='warehouse_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='出货仓库'),
        ),
        migrations.AlterField(
            model_name='stockinorder',
            name='is_complete',
            field=models.BooleanField(default=False, verbose_name='完成状态'),
        ),
        migrations.AlterField(
            model_name='stockinorder',
            name='is_void',
            field=models.BooleanField(default=False, verbose_name='是否作废'),
        ),
        migrations.AlterField(
            model_name='stockinorder',
            name='number',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='入库单号'),
        ),
        migrations.AlterField(
            model_name='stockinorder',
            name='order_no',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='来源单号'),
        ),
        migrations.AlterField(
            model_name='stockinorder',
            name='type',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='入库类型'),
        ),
        migrations.AlterField(
            model_name='stockinorder',
            name='warehouse_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='收货仓库'),
        ),
        migrations.AlterField(
            model_name='stockoutgoods',
            name='stock_out_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ptl.stockoutorder', verbose_name='出库工单'),
        ),
    ]
