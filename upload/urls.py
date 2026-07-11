from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('inventory/upload/', views.system_data_upload, name='hostdata_upload'),
    path('firewall/upload/', views.fw_data_upload, name='fwdata_upload'),

]