from django.test import TestCase
import unittest, re
from inventory.models import Inventory
from hosts.models import hosts
from inventory.jobs.minutely.update_inventory_table import Job as Job_update
from inventory.jobs.hourly.update_inventory import Job as Job_inventory


def setup_inventory_host(classArg, host='localhost', ):
    hosts.objects.create(hostname = host)
    return Job_update.execute(classArg)

def setup_inventory_table():

    Inventory.objects.create(
        host = "localhost", 
        ip = "1.2.3.4", 
        cores = 4, 
        ram = 4, 
        storage = '{"devices": [{"name": key,"size": size[0]}]}'
    )

    return Inventory.objects.last()

def get_ipvalidation(ip):

    regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
                25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
                25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
                25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$'''
        

    if(re.search(regex, ip)):  
        print("Valid IP address")  
        
    else:  
        print("Invalid IP address")  


class value_match:
    def __init__(self, value):
        self.value = value

class TestInventoryUpdater(TestCase):


    def test_add_hostname(self):
        """
        docstring
        """
        hosts.objects.create(hostname='localhost')
    
        self.assertWarnsMessage("Added 1 hosts to inventory tabel",Job_update.execute(self))

    def test_present_host(self):
        """
        docstring
        """
        text = setup_inventory_host(self)
        self.assertWarnsMessage(text,Job_update.execute(self))

class TestInventoryValues(TestCase):

    def test_get_host_facts(self):
        """
        docstring
        """
        setup_inventory_host(self)
        self.assertEqual(type(Job_inventory.get_server_facts(self, 'localhost')), dict)
    
    def test_get_expressions_linux(self):
        """
        docstring
        """

        setup_inventory_host(self)
        self.assertEqual(type(Job_inventory.get_fact_expressions(self, 'Linux')), list)

    def test_count_expressions_linux(self):

        list_elements = 6
        setup_inventory_host(self)
        
        self.assertEqual(len(Job_inventory.get_fact_expressions(self, 'Linux')), list_elements)

    def test_get_expressions_windows(self):
        """
        docstring
        """

        setup_inventory_host(self)
        self.assertEqual(type(Job_inventory.get_fact_expressions(self, 'Windows')), list)

    def test_count_expressions_windows(self):

        list_elements = 5
        setup_inventory_host(self)
        
        self.assertEqual(len(Job_inventory.get_fact_expressions(self, 'Windows')), list_elements)

    def test_update_db_linux(self):

        setup_inventory_host(self)

        match_count = 0
        match = [1,'1.2.3.4',8,'redhat', '8.2', 'Linux']
        system = 'Linux'
        host = 'localhost'
        expressions = [
            'memtotal_mb',
            'default_ipv4.address',
            'processor_count', 
            'os_family', 
            'distribution_version', 
            'ansible_system', 
            ]

        
        for test in range(len(expressions)):
            match_values = []
            match_values.append ( value_match(match[test]) )
            print(match_values[0].value)
            match_count += 1

            Job_inventory.update_inventory_db(self, match_values, system, host, expressions[test])
    
    def test_update_db_windows(self):

        setup_inventory_host(self)

        match_count = 0
        match = [1,'1.2.3.4',8,'Microsoft', 'Windows Server 2012']
        system = 'Windows'
        host = 'localhost'
        expressions = [
            'memtotal_mb',
            'ip_addresses',
            'processor_count', 
            'os_family', 
            'os_name'
            ]

        
        for test in range(len(expressions)):
            match_values = []
            match_values.append ( value_match(match[test]) )
            print(match_values[0].value)
            match_count += 1

            Job_inventory.update_inventory_db(self, match_values, system, host, expressions[test])
   
    def test_storage_localhost(self):
        """
        Docstring
        """

        setup_inventory_host(self)
        test_facts = Job_inventory.get_server_facts(self, 'localhost')

        Job_inventory.update_storage(self, test_facts, 'Linux', 'localhost')
class testModels(TestCase):
    """
    Docstring"
    """
    def test_inventory_models_host(self):
        """
        docstring
        """
        queryset = setup_inventory_table()       
        self.assertEqual(queryset.host, 'localhost')
    
    def test_inventory_models_IP(self):
        """
        docstring
        """
        queryset = setup_inventory_table()       
        self.assertWarnsMessage("Valid IP address", get_ipvalidation(queryset.ip))

if __name__ == '__main__':
    unittest.main()