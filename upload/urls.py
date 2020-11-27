from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('inventory/upload/', views.get_uploadData, name='hostdata_upload'),
    path('firewall/upload/', views.fw_data_upload, name='fwdata_upload'),

]