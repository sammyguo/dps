# Generated by Django 3.2.16 on 2024-11-29 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pda', '0002_stockoutrecord'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StockInRecord',
            new_name='GoodLocationRecord',
        ),
    ]