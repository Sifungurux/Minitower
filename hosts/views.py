from django.shortcuts import render
from .forms import AddHost
from .models import hosts

def add_host_create(request, *args, **kwargs):
    form = AddHost()
    print(*args, **kwargs)
    if request.method == 'POST':
        form = AddHost(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
        else:
            print(form.errors)
    context = {
        "form" : form
    }
    return render(request, "hosts/add_hosts.html", context)