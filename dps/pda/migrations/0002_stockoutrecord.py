# Generated by Django 3.2.16 on 2024-11-28 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pda', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockOutRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_code', models.CharField(blank=True, max_length=50, null=True, verbose_name='货物编码')),
                ('location_code', models.CharField(blank=True, max_length=32, null=True, verbose_name='库位编号')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '出库下架记录',
                'verbose_name_plural': '出库下架记录',
            },
        ),
    ]