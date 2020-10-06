from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .models import Inventory

row_num = Inventory.objects.all().count()


urlpatterns = [
    path('inventory/', views.index, name='index'),
    #path('inventory/profil/e', views.profile, name='profile'),
    path('profile/<str:hostname>', views.profile, name='profile')
]

