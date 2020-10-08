from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from hosts.models import hosts
from .models import configfile

# Create your views here.


def home(requests):
    # hostname = hosts.objects.all()
    # for host in hostname:
    #     hostname = str(host)
    #     f = open('config/difference/{}/file.txt.diff'.format(hostname), 'r')
    f = open('config/difference/localhost/file.txt.diff', 'r') # TODO Ændre så den valgte host og konfigurations fil vises.
    file_content = f.read()
    f.close()
    context = { 'file_content': file_content }
    return render(requests, 'config/home.html', context)

# def doc(request):
#     t = open('config/difference/localhost/file.txt.diff', 'r')
#     tfile_content = t.read()
#     t.close()
#     return HttpResponse(tfile_content, content_type="text/plain")