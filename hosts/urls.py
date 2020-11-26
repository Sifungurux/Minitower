from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'([\w|\W]+)/add-host/', views.add_host_create, name = 'add_host_create') ,
    path('add-host/', views.add_host_create, name = 'add_host_create')

]