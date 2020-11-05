from django.db import models
from hosts.models import hosts


class Inventory(models.Model):
    host = models.OneToOneField(hosts,on_delete=models.CASCADE, primary_key=True)
    #host = models.CharField('host name', primary_key=True,default=None, max_length=120)
    ip = models.CharField('IP Address', max_length=20)
    cores = models.IntegerField('Number of cores')
    ram = models.IntegerField('Amount of memory')
    storage = models.CharField('Total space in Giga as a list', max_length=120)
    os_family = models.CharField('OS family', max_length=50, default='RedHat')
    os_version = models.CharField('OS version', max_length=50, default='8')
    system = models.CharField('OS Type', max_length=20, default='Linux')

    def __str__(self):
        return self.name

        