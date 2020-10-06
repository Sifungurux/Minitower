from django.shortcuts import render
from django.http import HttpResponse
from .models import Inventory
from django.db.models import Q, Count
import json


def is_valid_queryparam(param):
    return param != '' and param is not None

def profile(request, hostname):
    qs = Inventory.objects.all()
    qs = qs.filter(name__iexact=hostname)
    
    for s in Inventory.objects.raw('SELECT * FROM inventory_inventory WHERE name = %s', [hostname]):
        json_obj = s.storage
        storage_qs = json.loads(json_obj)
    """
    Test json
    {
        "devices": [
            {
            "name": "sda", 
            "size": "60.00 GB"
            },
            {
            "name": "sdb", 
            "size": "60.00 GB"
            }
        ]
    }

    """
    context = {
        'title': hostname,
        'hosts': qs,
        'storage': storage_qs['devices'],
    }
    return render(request, 'inventory/host_profile.html', context )

def index(request):
    title = "Host Overview"
    qs = filter(request)
    context = {
        'title': title,
        'queryset': qs
    }
    return render(request, 'inventory/inventory_base.html', context)
    #hosts = Inventory.objects.all()
    #return render(request, 'inventory/inventory_base.html',{'title': title, 'hosts':hosts})

def filter(request):
    qs = Inventory.objects.all()
    host_query = request.GET.get('host_search')
    if is_valid_queryparam(host_query):
        qs = qs.filter(
            Q(name__icontains=host_query)   |
            Q(systemtype__icontains=host_query)  |
            Q(os_family__icontains=host_query)  |
            Q(os_version__icontains=host_query)
        ).distinct()
    return qs
