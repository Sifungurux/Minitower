import subprocess
import json
from jsonpath_ng import jsonpath, parse
from hosts.models import hosts
from inventory.models import Inventory
from django_extensions.management.jobs import HourlyJob


class Job(HourlyJob):

    def get_port_status(self, hostname):
        port = [22,3389]
        for p in range(len(port)):
            ansible_output = subprocess.Popen(['nc', '-zvw1', hostname , str(port[p])], 
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
            stdout, stderr = ansible_output.communicate()
            stdout = stdout.decode()
            if 'open' in stdout:
                print("Using port {} to connect to host".format(str(port[p])))
                hosts.objects.filter(hostname=hostname).update(connectiontype=port[p])
                if port[p] == 22:
                    Inventory.objects.filter(host=hostname).update(system='Linux')
                elif port[p] == 3389:
                    Inventory.objects.filter(host=hostname).update(system='Windows')



    #get_port_status("infappudv01.ccta.dk")


    def get_server_state(self, hostname):
        """
        Gets server facts from server, splits output, load and returns json data
        Args:
            hostname (string): Name of host to get facts from

        Returns:
            json_object: Json_object containing server data
        """
        ansible_output = subprocess.Popen(['ansible', hostname, '-m', 'ping', '-o'],
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.STDOUT)
        stdout, stderr = ansible_output.communicate()
        stdout = stdout.decode()
        json_data = stdout.split('=>')
        return json.loads(json_data[1])


    def set_server_state(self, hostname):

        get_state = self.get_server_state(hostname)
        state = json.dumps(get_state['ping'])
        if 'pong' in state:
            state = "Connected"
        else:
            state = "Not Connected"
        hosts.objects.filter(hostname=hostname).update(server_status=state) 
        return "{} in {} state".format(hostname, state)

    def execute(self):
        for host in hosts.objects.all():
            print(self.set_server_state(str(host)))
            self.get_port_status(str(host))