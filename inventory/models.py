from django.db import models
from hosts.models import hosts


class Inventory(models.Model):
    host = models.ForeignKey(hosts, default=1, on_delete=models.SET_DEFAULT)
    ip = models.CharField('IP Address', max_length=20)
    cores = models.IntegerField('Number of cores')
    ram = models.IntegerField('Amount of memory')
    storage = models.CharField('Total space in Giga as a list', max_length=120)
    os_family = models.CharField('OS family', max_length=20, default='RedHat')
    os_version = models.CharField('OS version', max_length=20, default='8')
    system = models.CharField('OS Type', max_length=20, default='Linux')


    def __str__(self):
        return self.name

        