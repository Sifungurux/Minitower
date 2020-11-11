from django.db import models


PROTOCOLS = (
    (u'1', u'TCP'),
    (u'2', u'UDP'),
    (u'3', u'FTP'),
)
class firewall(models.Model):
    source = models.CharField("Source IP or subnet",max_length = 100)
    sourcenat = models.CharField("Source NAT IP", max_length = 100)
    dest = models.CharField("Destination IP or subnet", max_length = 100)
    destnat = models.CharField("Destination NAT IP", max_length = 100)
    port = models.CharField("Destination port", max_length = 100)
    protocol = models.CharField(max_length=1, choices = PROTOCOLS)
    oldfwid = models.CharField("Current infastructor id", max_length = 100)
    fwid = models.CharField("Firewll id for firewall rule", max_length = 100)
    description = models.CharField("Firewall descriptions", max_length = 1000)
    ticket = models.CharField("Ticket nr. for fw connection", max_length = 100)
    status = models.CharField("Status for fw ",max_length = 100)
    note = models.CharField("Note", max_length = 1000)
