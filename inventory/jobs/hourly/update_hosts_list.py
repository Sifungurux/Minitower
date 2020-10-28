import subprocess
import json
from jsonpath_ng import jsonpath, parse
from hosts.models import hosts
from inventory.models import Inventory
from django_extensions.management.jobs import HourlyJob


class Job(HourlyJob):

    def get_port_status(self):
        port = [22,3389]
        linux_hosts = []
        win_hosts = []
        for  hostname in hosts.objects.all():
            hostname = str(hostname)
            for p in range(len(port)):
                ansible_output = subprocess.Popen(['nc', '-zvw1', hostname , str(port[p])], 
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT)
                stdout, stderr = ansible_output.communicate()
                stdout = stdout.decode()
                if 'open' in stdout:
                    if port[p] == 22:
                        Inventory.objects.filter(host=hostname).update(system='Linux')
                        hosts.objects.filter(hostname=hostname).update(connectiontype=22)
                        linux_hosts.append(hostname)
                    elif port[p] == 3389:
                        Inventory.objects.filter(host=hostname).update(system='Windows')
                        hosts.objects.filter(hostname=hostname).update(connectiontype=5985)
                        win_hosts.append(hostname)

        self.set_dynamic_inventory(linux_hosts, win_hosts)


    def set_dynamic_inventory(self, linux_hosts, win_hosts):
        inventoryfile = open("inventory.txt", "w")
        inventoryfile.writelines("[linux]\n")
        for host in linux_hosts:
            inventoryfile.write("{}\n".format(host))
        inventoryfile.writelines("\n[windows]\n")
        for host in win_hosts:
            inventoryfile.write("{}\n".format(host))

        inventoryfile.close()
    def get_server_state(self, hostname):
        """
        Gets server facts from server, splits output, load and returns json data
        Args:
            hostname (string): Name of host to get facts from

        Returns:
            json_object: Json_object containing server data
        """
        ansible_output = subprocess.Popen(['ansible', hostname, '-m', 'setup', '-o'],
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.STDOUT)
        stdout, stderr = ansible_output.communicate()
        stdout = stdout.decode()
        if 'UNREACHABLE!' in stdout:
            return 'unreachable'
        else:   
            json_data = stdout.split('=>')
            return json.loads(json_data[1])


    def set_server_state(self, hostname):

        get_state = self.get_server_state(hostname)
        if 'unreachable' not in get_state:
            state = "Connected"
        else:
            state = "Not Connected"
        hosts.objects.filter(hostname=hostname).update(server_status=state) 
        return "{} in {} state".format(hostname, state)

    def execute(self):
        self.get_port_status()
        for host in hosts.objects.all():
            print(self.set_server_state(str(host)))
