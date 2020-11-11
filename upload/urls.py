from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('inventory/upload/', views.simple_upload, name='hostdata_upload'),
]