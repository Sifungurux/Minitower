from django.db import models
from django.utils import timezone
from hosts.models import hosts

# Create your models here.


# class configid(models.Model):
#     hostid = models.ForeignKey(hosts, default=1, on_delete=models.SET_DEFAULT)
#     cid = models.AutoField('config id', primary_key=True)
#     description = models.TextField('Give a short description', max_length=200, blank=True)

#     def __str__(self):
#         return str(self.cid)


class configfile(models.Model):
    hostid = models.ForeignKey(hosts, default=1, on_delete=models.SET_DEFAULT)
    cid = models.AutoField('config id', primary_key=True)
    configfile_path = models.CharField('Config file full path on remote host', max_length=200)
    configfile_name = models.CharField('Config file name with extention', max_length=100)
    pf_stat = models.FileField('preferred file stat', upload_to='config/configfiles/')
    diff_pf_stat = models.FileField('Difference between preferred file and remote file', upload_to='config/difference/', blank=True)
    description = models.TextField('Give a short description', max_length=200, blank=True)

    def __str__(self):
        return str(self.configfile_name)