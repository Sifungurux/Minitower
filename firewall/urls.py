from django.urls import path
from . import views

urlpatterns = [
    path('firewall/', views.get_firewall_list, name = 'get_firewall_list')
]