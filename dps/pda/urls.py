from django.urls import path,include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from pda import views
from pda.views import StockInRecordViewSet

app_name = 'pda'

router = DefaultRouter()
router.register(r'good_location_record', StockInRecordViewSet, 'good_location_record')
router.register(r'stock_out_record', views.StockOutRecordViewSet, 'stock_out_record')

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('stock_in/<int:pk>/', views.stockin, name='stock_in'),
    path('stock_out/<int:pk>/', views.stockout, name='stock_out'),
    path('stock_in_record_list/', views.StockInRecordListView.as_view(), name='stock_in_record_list'),
    path('stock_out_record_list/', views.StockOutRecordListView.as_view(), name='stock_out_record_list'),

    # API
    path('pda/', include(router.urls)),
]