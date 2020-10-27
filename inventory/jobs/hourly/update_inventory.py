import json
import os
import subprocess
import sys

from django_extensions.management.jobs import HourlyJob
from inventory.models import Inventory
from hosts.models import hosts

from jsonpath_ng import jsonpath, parse


class Job(HourlyJob):
    """
        Get hostname from db to run ansible -m setup <hostname> it then saves the ansible json output in a variable
        And that variable take out elements and save them to db
        Uses Jobs scheduling from the django extenstion package.

        Consist of on function for executing the scheduling job. 
    """

    def get_server_facts(self, host):
        """
        Gets server facts from server, splits output, load and returns json data
        Args:
            host (string): Name of host to get facts from

        Returns:
            json_object: Json_object containing server data
        """
        try:
            ansible_output = subprocess.Popen(['ansible', host, '-m', 'setup', '-o'],
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.STDOUT)
            stdout, stderr = ansible_output.communicate()
            stdout = stdout.decode()

            json_data = stdout.split('=>')
            return json.loads(json_data[1])
        except IndexError: 
            return 'unreachable'

    def get_fact_expressions(self, system):
        """
        Function defines search expression

        Args:
            system (string): System name eg. Linux or Windows

        Returns:
            list: Returns list of search expressios for match json objects
        """
        if "Linux" == system:
            fact_expressions = [
                '$.ansible_facts.ansible_memtotal_mb',          # Total memory
                '$.ansible_facts.ansible_default_ipv4.address',  # IPv4 Address<
                '$.ansible_facts.ansible_processor_count',
                '$.ansible_facts.ansible_os_family',
                '$.ansible_facts.ansible_distribution_version',
                '$.ansible_facts.ansible_system',
                '$.ansible_facts.ansible_system_vendor',
            ]

        if "Windows" == system:
            fact_expressions = [
                '$.ansible_facts.ansible_memtotal_mb',          # Total memory
                '$.ansible_facts.ansible_ip_addresses',         # IPv4 Address<
                '$.ansible_facts.ansible_processor_count',
                '$.ansible_facts.ansible_os_family',
                '$.ansible_facts.ansible_os_name',
                '$.ansible_facts.ansible_system_vendor',
                '$.ansible_facts.ansible_owner_name',
            ]
        return fact_expressions

    def update_inventory_db(self, match, system, host, expressions):         
        """
        Updates db with based on system name.

        Args:
            match (list): Contains list of values match with a defind expression
            system (string): System type
            host (string): 
            expressions (string): Contains a predefind search string for matching values
        """
        if "Linux" == system:
            if 'mem' in expressions:
                print("Updating memory..."), Inventory.objects.filter(
                    host=host).update(ram=match[0].value)
            if 'address' in expressions:
                print("Updating IP-Address..."), Inventory.objects.filter(
                    host=host).update(ip=match[0].value)
            if 'processor_count' in expressions:
                print("Updating CPU Cores..."), Inventory.objects.filter(
                    host=host).update(cores=match[0].value)
            if 'os_family' in expressions:
                print("Updating OS Name..."), Inventory.objects.filter(
                    host=host).update(os_family=match[0].value)
            if 'distribution_version' in expressions:
                print("Updating OS Version..."), Inventory.objects.filter(
                    host=host).update(os_version=match[0].value)
            if 'vendor' in expressions:
                print("Updating System vendor..."), hosts.objects.filter(
                    hostname=host).update(system_vendor=match[0].value) 
            if '$.ansible_facts.ansible_system' == expressions:
                print("Updating System Name..."), Inventory.objects.filter(
                    host=host).update(system=match[0].value)
     

        if "Windows" == system:
            if 'mem' in expressions:
                print("Updating memory..."), Inventory.objects.filter(
                    host=host).update(ram=match[0].value)
            if 'address' in expressions:
                print("Updating IP-Address..."), Inventory.objects.filter(
                    host=host).update(ip=match[0].value[0])
            if 'processor_count' in expressions:
                print("Updating CPU Cores..."), Inventory.objects.filter(
                    host=host).update(cores=match[0].value)
            if 'os_family' in expressions:
                print("Updating System Name..."), Inventory.objects.filter(
                    host=host).update(system=match[0].value)
            if 'os_name' in expressions:
                get_name = match[0].value

                get_name = get_name.split('Windows')
                print("Updating OS Name..."), Inventory.objects.filter(
                    host=host).update(os_family=get_name[0])
                print("Updating OS Version..."), Inventory.objects.filter(
                    host=host).update(os_version=get_name[1])
            if 'ansible_system_vendor' in expressions:
                print("Updating System vendor..."), hosts.objects.filter(
                    hostname=host).update(system_vendor=match[0].value)
            if 'ansible_system_vendor' in expressions:
                print("Updating System owner..."), hosts.objects.filter(
                    hostname=host).update(system_owner=match[0].value)    

    def update_storage(self, facts_data, system, host):
        """
        Updates storage for Linux and calls to update windows storage

        Args:
            facts_data (Json_object): Json object containing a output from ansible command
            system (String): System type (Linux or Windows)
            host (String): Name of host 
        """
        devices_size = {"devices": []}
        if "Linux" == system:
            for key, device in facts_data['ansible_facts']['ansible_devices'].items():
                if 'sd' in key:
                    size = device['size'].split(' ')
                    devices_size["devices"].append({
                        "name": key,
                        "size": size[0]
                    })
            devices_size = json.dumps(devices_size, indent=2)
            Inventory.objects.filter(host=host).update(storage=devices_size)
        if "Windows" == system:
            self.get_windows_disc_facts(host)

    def get_windows_disc_facts(self, host):
        """
        Gets disc facts from a windows server and with a whlie-loop gets all devices size in GB
        Uses the an error "IndexError" when it is out of range and breaks loop. 
        Write information about disc information to db in a json format

        Args:
            host (Inventory object): Contains name of server that is been processed.

        Returns: Nothing but write result to db
        """
        devices_size = {"devices": []}
        ansible_cmd = subprocess.Popen(['ansible', str(host), '-m', 'win_disk_facts', '-o'],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT)
        stdout, stderr = ansible_cmd.communicate()
        stdout = stdout.decode()
        json_data = stdout.split('=>')
        disc_data = json.loads(json_data[1])
        set_db_disk = True
        device = 0
        while set_db_disk:
            try:
                device_letter = disc_data['ansible_facts']['ansible_disks'][device]['partitions'][0]['access_paths'][0]
                print(device_letter)
                device_letter = device_letter.split(':')
                print("test 1")
                disc_size = disc_data['ansible_facts']['ansible_disks'][device]['size']
                disc_size = round(disc_size / (1024 * 1024 * 1024), 3)
            
                print(disc_size , device_letter)
                devices_size["devices"].append({
                    "name": str(device_letter[0]),
                    "size": float(disc_size)
                    })


                device += 1
             
            except IndexError:
                set_db_disk = False
        
        devices_size = json.dumps(devices_size, indent=2)
        Inventory.objects.filter(host=host).update(storage=devices_size)                    

            
    def execute(self):
        """
        Main function
        Loops though hosts in database to get predefined information about hardware.

        Takes no arguments

        Prints out information of updates servers 
        """
        print("Cronjob køre!!")
        hosts_update = 0
        for host in hosts.objects.all():
            facts_data = self.get_server_facts(str(host))
            try:
                print("Getting system name")

                if "Linux" == facts_data['ansible_facts']['ansible_system']:
                    os_system = 'Linux'
                else:
                    os_system = "Windows"
                print("Starting update of inventory")
                for expressions in self.get_fact_expressions(os_system):
                    jsonpath_expression = parse(expressions)
                    match = jsonpath_expression.find(facts_data)
                    self.update_inventory_db(match, os_system, host, expressions)

                self.update_storage(facts_data, os_system, host)
                print("Host:{} - Updated".format(str(host)))
                hosts_update += 1
            except TypeError: 
                continue
        print("Number of hosts updated: {}".format(hosts_update))
