from django.db import models


PROTOCOLS = (
    (u'TCP', u'TCP'),
    (u'UDP', u'UDP'),
)
class firewall(models.Model):
    source = models.CharField("Source IP or subnet",max_length = 100)
    sourcenat = models.CharField("Source NAT IP", max_length = 100, null = True, blank = True)
    dest = models.CharField("Destination IP or subnet", max_length = 100)
    destnat = models.CharField("Destination NAT IP", max_length = 100 , null = True, blank = True)
    port = models.CharField("Destination port", max_length = 100)
    protocol = models.CharField(max_length=5, choices = PROTOCOLS)
    ref = models.CharField("ref for infastructor id", max_length = 100, default = 'unset')
    description = models.CharField("Firewall descriptions", max_length = 1000)
    ticket = models.CharField("Ticket nr. for fw connection", max_length = 100)
    status = models.CharField("Status for fw ",max_length = 100)
    note = models.CharField("Note", max_length = 1000)

    def __str__(self):
        return self.source + " | " + self.dest + " | " + self.port