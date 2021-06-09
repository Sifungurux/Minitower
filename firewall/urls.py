from django.urls import path, re_path
from . import views

urlpatterns = [
    path('firewall/', views.get_firewall_list, name = 'get_firewall_list'),
    re_path(r'([\w|\W]+)/add-firewall/', views.add_fw_create, name = 'add_fw_create') ,
    path('add-firewall/', views.add_fw_create, name = 'add_fw_create'),
    path('create/', views.AddModalFirewallView.as_view(), name='create_firewall_rule'),
    path('fwrule/<int:id>', views.get_fwrule, name='get_fwrule')
]