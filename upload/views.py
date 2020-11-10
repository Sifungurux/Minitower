from django.shortcuts import render
from django.http import HttpResponse
from django.db import IntegrityError
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from datetime import datetime
import os, socket
from csv import DictReader

import shared_functions.hosts as hostname_check
from hosts.models import hosts

def simple_upload(request):

    now = datetime.now()
    timetag = now.strftime("%d%m%Y-%H%M")

    if request.method == 'POST' and request.FILES['systemdata']:
        systemdata = request.FILES['systemdata']
        fs = FileSystemStorage()

        file_name, file_extension = os.path.splitext(systemdata.name)
        systemdata.name = f"system-data-{timetag}{file_extension}"
        filename = fs.save(systemdata.name, systemdata)
        uploaded_file_url = fs.url(filename)
        msg = set_system_data(filename)

        guide = "Guide to upload valid system data to the system.\n Fields define:\nHostname and a description"
        context = {
            'title': "System data upload",
            'uploaded_file_url': uploaded_file_url,
            'msg': msg
        }

        return render(request, 'upload/simple_upload.html', context)
    return render(request, 'upload/simple_upload.html')

def set_system_data(f):
    error_list = []
    with open(f"data/{f}", 'r', newline='', encoding='utf-8-sig') as read_obj:
        csv_dict_reader = DictReader(read_obj,dialect='excel', delimiter=';')
        for row in csv_dict_reader:

            if hostname_check.is_fqdn(row['hostname']):
                try: 
                    socket.gethostbyname(row['hostname'])
                    
                    hostname = row['hostname']
                    description = row['description']
                    if 'systemproduct' in row: systemproduct = row['systemproduct']
                    else: systemproduct = '-'

                    if 'systemtype' in row: systemtype = row['systemtype']
                    else: systemtype = '-'

                    if 'server_status' in row: server_status = row['server_status']
                    else: server_status = '-'

                    if 'environment' in row: environment = row['environment']
                    else: environment = '-'

                    if 'connectiontype' in row: connectiontype = row['connectiontype']
                    else: connectiontype = 22

                    if 'system_owner' in row: system_vendor = row['system_vendor']
                    else: system_vendor = '-'

                    if 'system_owner' in row:  system_owner = row['system_owner']
                    else: system_owner = ''
                    
                    try:
                        hosts.objects.create(
                            hostname = hostname, 
                            description = description, 
                            systemproduct = systemproduct, 
                            systemtype = systemtype, 
                            server_status = server_status,
                            environment = environment,
                            connectiontype = connectiontype,
                            system_vendor = system_vendor,
                            system_owner = system_owner
                        )  
                    except IntegrityError :
                        print(f"Server with hostname: {row['hostname']} allready exist" )
                        error_list.append(f"Server with hostname: {row['hostname']} allready exist" )
                except socket.gaierror:
                    print(f"Server with hostname: {row['hostname']} is invalid or server is not live")
                    error_list.append(f"Server with hostname: {row['hostname']} is invalid or server is not live")
                    
            


    if len(error_list) == 0:
        error_list.append("Not errors incounted")
    return error_list