from django.db import models

# Create your models here.

class hosts(models.Model):
    hostname = models.CharField('Hostname', max_length=50, primary_key=True)
    description = models.TextField('Short description', max_length=200, blank=True)
    systemproduct = models.CharField('One word system name e.g informatica, hdp or so on ...', max_length=120 , default='PD_infra')
    systemtype = models.CharField('system Function name e.g application, Database and so on ...', max_length=120 , default='PD_infra')
    server_status = models.CharField('Status field for it Ansible can connect to server', max_length=30, default='Not Connected')
    environment = models.CharField('Server environment', max_length=30, default='udv')
    connectiontype = models.IntegerField('Port number to connect', default=22)
    vendor = models.CharField('System vendor information', max_length=30, default='-')
    supplier = models.CharField('System owner information', max_length=30, default='DVU')

    def __str__(self):
        return self.hostname

class navnstdproduct(models.Model):
    product = models.CharField("Product short name", max_length=3)
    Product_description = models.CharField("Full product name", max_length=100)

    def __str__(self):
        return self.product

class navnstdenv(models.Model):
    env = models.CharField("Environment short name", max_length=3)
    env_description = models.CharField("Full Environment name", max_length=100)

    def __str__(self):
        return self.env

class navnstdrole(models.Model):
    role = models.CharField("Role short name", max_length=3)
    role_description = models.CharField("Role name", max_length=100)

    def __str__(self):
        return self.role
"""
class connectivity(models.Model):
    connection_id = models.OneToOneField(hosts,on_delete=models.CASCADE, primary_key=True)
    server_status = models.CharField('Status field for it Ansible can connect to server', max_length=30, default='Not Connected')
    connectiontype = models.IntegerField('Port number to connect', default=22)

class systeminformation(models.Model):
    system_id = models.OneToOneField(hosts,on_delete=models.CASCADE, primary_key=True)
    system_vendor = models.CharField('System vendor information', max_length=30)
    system_owner = models.CharField('System vendor information', max_length=30, default='DVU')

class systemowner(models.Model):
    owner_id = models.OneToOneField(hosts,on_delete=models.CASCADE, primary_key=True)
    owener = models.CharField('Owner', max_length=30, default='DVU')
"""