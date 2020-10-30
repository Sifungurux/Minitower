from django_extensions.management.jobs import HourlyJob
from hosts.models import hosts
from hosts.models import navnstdproduct, navnstdrole, navnstdenv
from django.db import IntegrityError


class Job(HourlyJob):
    help = "My sample job."

    def execute(self):
        n = 3
        try:
            for host in  hosts.objects.all():
                hostname = str(host).split('.')
                namespace = [(hostname[0][i:i+n]) for i in range(0, len(hostname[0]), n)]
                # executing empty sample job
                Product_description = navnstdproduct.objects.filter(product=str(namespace[0])).values('Product_description')
                role_description = navnstdrole.objects.filter(role=str(namespace[1])).values('role_description')
                env_description = navnstdenv.objects.filter(env=str(namespace[2])).values('env_description')

                hosts.objects.filter(hostname=host).update(systemproduct=Product_description)                    
                hosts.objects.filter(hostname=host).update(systemtype=role_description)                    
                hosts.objects.filter(hostname=host).update(environment=env_description)                    
        except IntegrityError:
            print(f"Host name - {hostname[0]} - does not follow naming conventions")