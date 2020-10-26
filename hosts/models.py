from django.db import models

# Create your models here.

class hosts(models.Model):
    hostname = models.CharField('Hostname', max_length=50, primary_key=True)
    description = models.TextField('Give a short description', max_length=200, blank=True)
    systemtype = models.CharField('Give a one word system name e.g informatica, hdp or so on ...', max_length=120 , default='PD_infra')
    server_status = models.CharField('Status field for it Ansible can connect to server', max_length=30, default='Not Connecte')
    connectiontype = models.IntegerField('Port number to connect', default=22)

    def __str__(self):
        return self.hostname