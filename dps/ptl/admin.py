from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'warehouse']

@admin.register(Label)

class LabelAdmin(admin.ModelAdmin):
    pass
