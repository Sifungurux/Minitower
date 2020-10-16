from django_extensions.management.jobs import MinutelyJob
from hosts.models import hosts
from inventory.models import Inventory
from django.db import IntegrityError

class Job(MinutelyJob):
    help = "My sample job."

    def execute(self):
        hostinfo = Inventory.objects.all()
        host_count_update = 0
        for hostname in hosts.objects.all():
            try:
                Inventory.objects.create(host=hostname, cores=0, ram=0, os_version='-', os_family='-', system='-')
                print('Updating db with host: {}'.format(hostname))
                host_count_update +=1
            except IntegrityError:
                continue


        print("Added {} hosts to inventory tabel".format(host_count_update))

