from django.shortcuts import render
from django.http import HttpResponse
from .models import firewall

from django.db.models import Q, Count

from .forms import AddFirewall

def is_valid_queryparam(param):
    return param != '' and param is not None


def get_firewall_list(request):
    title = "Firewall Overview"
    qs = filter(request)
    print(str(qs.query))
    context = {
        'title': title,
        'queryset': qs
    }
    return render(request, 'firewall/firewall_base.html', context)

def filter(request):
    qs = firewall.objects.all()
    fw_query = request.GET.get('fw_search')
    if is_valid_queryparam(fw_query):
        qs = qs.filter(
            Q(source__icontains=fw_query)                       |
            Q(sourcenat__icontains=fw_query)                    |
            Q(dest__icontains=fw_query)                         |
            Q(destnat__icontains=fw_query)              |
            Q(port__icontains=fw_query)                         |
            Q(oldfwid__icontains=fw_query)                      |
            Q(fwid__icontains=fw_query)                         |
            Q(ticket__icontains=fw_query)                       |
            Q(status__icontains=fw_query)                       
        ).distinct()
    return qs

def add_fw_create(request, *args, **kwargs):
    form = AddFirewall()
    title = "Add firewall rule"
    print(*args, **kwargs)
    if request.method == 'POST':
        print(request.POST['validate'])
        if "validate" == request.POST['validate'].lower():
            form = AddFirewall(request.POST)
            if form.is_valid():
                print(form.cleaned_data)
            else:
                print(form.errors)
    context = {
        "title": title,
        "form" : form
    }
    return render(request, "firewall/add_firewall.html", context)