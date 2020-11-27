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
from firewall.models import firewall

from .forms import UploadData


now = datetime.now()
timetag = now.strftime("%d%m%Y-%H%M")

def get_uploadData(request, *args, **kwargs):
    form = UploadData()
    title = "Data upload"
    print(*args, **kwargs)
    if request.method == 'POST':
        form = UploadData(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
        else:
            print(form.errors)
    context = {
        "title": title,
        "form" : form
    }
    return render(request, "upload/host-data-upload.html", context)

def system_data_upload(request):

    now = datetime.now()
    timetag = now.strftime("%d%m%Y-%H%M")
    title = "System data upload"

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
            'title': title,
            'uploaded_file_url': uploaded_file_url,
            'msg': msg
        }
        return render(request, 'upload/host-data-upload.html', context)
    return render(request, 'upload/host-data-upload.html')

def fw_data_upload(request):
    title = "Firewall data upload"

    if request.method == 'POST' and request.FILES['fwdata']:
        fwdata = request.FILES['fwdata']
        fs = FileSystemStorage()

        file_name, file_extension = os.path.splitext(fwdata.name)
        fwdata.name = f"fw-data-{timetag}{file_extension}"
        filename = fs.save(fwdata.name, fwdata)
        uploaded_file_url = fs.url(filename)
        msg = set_fw_data(filename)

        guide = "Guide to upload valid fw data to the system.\n Fields define:\Source, destination, port and sysntem"
        context = {
            'title': title,
            'uploaded_file_url': uploaded_file_url,
            'msg': msg
        }

        return render(request, 'upload/fw-data-upload.html', context)
    return render(request, 'upload/fw-data-upload.html')

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

def set_fw_data(f):
    error_list = []
    with open(f"data/{f}", 'r', newline='', encoding='utf-8-sig') as read_obj:
        csv_dict_reader = DictReader(read_obj,dialect='excel', delimiter=';')
        fw_rules = firewall.objects.all()
        for row in csv_dict_reader:
            source = row['src']
            dest = row['dest']
            port = row['port']
            protocol = row['protocol']
            ticket = row['Ticket']
            description = row['Description']


            if 'Source NAT' in row: sourcenat = row['source nat']
            else: sourcenat = '-'

            if 'Dest NAT' in row: destnat = row['dest nat']
            else: destnat = '-'

            if 'ref' in row: ref = row['ref']
            else: ref = 'unset'

            if 'status' in row: system_vendor = row['staus']
            else: status = 'unclear'

            if 'notat' in row:  system_owner = row['note']
            else: note = ''
            

            if ref == 'unset':
                try:
                    firewall.objects.create(
                        source = source, 
                        dest = dest, 
                        port = port, 
                        ticket = ticket, 
                        description = description,
                        sourcenat = sourcenat,
                        destnat = destnat,
                        protocol = protocol,
                        ref = ref,
                        status = status,
                        note = note
                    )  
                except IntegrityError :
                    print(f"FW rule allready exist" )
                    error_list.append(f"Firewall rule: {source} allready exist" )
            if ref is not 'unset':
                for id_nr in fw_rules: 
                    fw_entry = firewall.objects.get(id=id_nr)
                    if fw_entry.source == row['src'] and fw_entry.dest == row['dest'] and fw_entry.port == row['port'] and ref == row['ref']:
                        print(f"FW rule {source} -> {dest}:{port} with {ref} allready exist" )
                        continue
                    else:
                        try:
                            firewall.objects.create(
                            source = source, 
                            dest = dest, 
                            port = port, 
                            ticket = ticket, 
                            description = description,
                            sourcenat = sourcenat,
                            destnat = destnat,
                            protocol = protocol,
                            ref = ref,
                            status = status,
                            note = note
                            )  
                        except IntegrityError:
                            error_list.append(IntegrityError)

    if len(error_list) == 0:
        error_list.append("Not errors incounted")
    return error_list