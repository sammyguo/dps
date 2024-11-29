from django.urls import path
from django.views.generic import TemplateView
import ptl.views as views

from .views import (
    WarehouseListView, WarehouseCreateView, WarehouseUpdateView, WarehouseDeleteView,
    LocationListView, LocationCreateView, LocationUpdateView, LocationDeleteView,
    LabelListView, LabelCreateView, LabelUpdateView, LabelDeleteView,
    StockInOrderListView, StockInOrderCreateView, StockInOrderUpdateView, StockInOrderDeleteView,
    StockOutOrderListView, StockOutOrderCreateView, StockOutOrderUpdateView,StockOutOrderDeleteView
)

app_name = 'ptl'

urlpatterns = [
    # 首页
    path('', TemplateView.as_view(template_name='ptl/index.html'), name='home'),

    path('warehouses/', WarehouseListView.as_view(), name='warehouse_list'),
    path('warehouses/create/', WarehouseCreateView.as_view(), name='warehouse_create'),
    path('warehouses/update/<int:pk>/', WarehouseUpdateView.as_view(), name='warehouse_update'),
    path('warehouses/delete/<int:pk>/', WarehouseDeleteView.as_view(), name='warehouse_delete'),

    # Location URLs
    path('locations/', LocationListView.as_view(), name='location_list'),
    path('locations/create/', LocationCreateView.as_view(), name='location_create'),
    path('locations/update/<int:pk>/', LocationUpdateView.as_view(), name='location_update'),
    path('locations/delete/<int:pk>/', LocationDeleteView.as_view(), name='location_delete'),

    # Label URLs
    path('labels/', LabelListView.as_view(), name='label_list'),
    path('labels/create/', LabelCreateView.as_view(), name='label_create'),
    path('labels/update/<int:pk>/', LabelUpdateView.as_view(), name='label_update'),
    path('labels/delete/<int:pk>/', LabelDeleteView.as_view(), name='label_delete'),

    path('stock_in_order/', StockInOrderListView.as_view(), name='stock_in_order_list'),
    path('stock_in_order/create/', StockInOrderCreateView.as_view(), name='stock_in_order_create'),
    path('stock_in_order/update/<int:pk>/', StockInOrderUpdateView.as_view(), name='stock_in_order_update'),
    path('stock_in_order/delete/<int:pk>/', StockInOrderDeleteView.as_view(), name='stock_in_order_delete'),

    path('stock_out_order/', StockOutOrderListView.as_view(), name='stock_out_order_list'),
    path('stock_out_order/create/', StockOutOrderCreateView.as_view(), name='stock_out_order_create'),
    path('stock_out_order/update/<int:pk>/', StockOutOrderUpdateView.as_view(), name='stock_out_order_update'),
    path('stock_out_order/delete/<int:pk>/', StockOutOrderDeleteView.as_view(), name='stock_out_order_delete'),

    # 标签亮灯测试
    path('label_light_test/', views.label_light_test, name='label_light_test'),
    path('single_label_light_test/<int:label_id>/<str:cmd>/<str:mode>/', views.single_label_light_test, name='single_label_light_test'),
    path('group_label_light_test/', views.group_label_light_test, name='group_label_light_test'),
]
