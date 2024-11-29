# Generated by Django 3.2.16 on 2024-11-27 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ptl', '0008_auto_20241127_1019'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stockingoods',
            options={'verbose_name': '入库货品', 'verbose_name_plural': '入库货品'},
        ),
        migrations.AlterModelOptions(
            name='stockinorder',
            options={'verbose_name': '入库任务工单', 'verbose_name_plural': '入库任务工单'},
        ),
        migrations.AlterModelOptions(
            name='stockoutgoods',
            options={'verbose_name': '出货货品', 'verbose_name_plural': '出货货品'},
        ),
        migrations.AlterModelOptions(
            name='stockoutorder',
            options={'verbose_name': '出库任务工单', 'verbose_name_plural': '出库任务工单'},
        ),
        migrations.RenameField(
            model_name='stockinorder',
            old_name='order_no',
            new_name='src_order',
        ),
        migrations.RenameField(
            model_name='stockoutorder',
            old_name='order_no',
            new_name='src_order',
        ),
        migrations.AlterField(
            model_name='stockingoods',
            name='supplier_batch',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='厂商批次'),
        ),
        migrations.AlterField(
            model_name='stockinorder',
            name='number',
            field=models.CharField(blank=True, max_length=32, null=True, unique=True, verbose_name='入库单号'),
        ),
        migrations.AlterField(
            model_name='stockoutgoods',
            name='supplier_batch',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='厂商批次'),
        ),
    ]