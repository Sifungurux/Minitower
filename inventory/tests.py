from django.test import TestCase
import unittest
from inventory.models import Inventory
from hosts.models import hosts
from inventory.jobs.minutely.update_inventory_table import Job as Job_update
from inventory.jobs.hourly.update_inventory import Job as Job_inventory


def setup_inventory_table(classArg, host='localhost', ):
    hosts.objects.create(hostname = host)
    return Job_update.execute(classArg)


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
        text = setup_inventory_table(self)
        self.assertWarnsMessage(text,Job_update.execute(self))

class TestInventoryValues(TestCase):

    def test_present_host(self):
        """
        docstring
        """
        setup_inventory_table(self)
        self.assertEqual(type(Job_inventory.get_server_facts(self, 'localhost')), dict)
    
    def test_get_expressions_linux(self):
        """
        docstring
        """

        setup_inventory_table(self)
        self.assertEqual(type(Job_inventory.get_fact_expressions(self, 'Linux')), list)

    def test_count_expressions_linux(self):

        list_elements = 6
        setup_inventory_table(self)
        
        self.assertEqual(len(Job_inventory.get_fact_expressions(self, 'Linux')), list_elements)

    def test_get_expressions_windows(self):
        """
        docstring
        """

        setup_inventory_table(self)
        self.assertEqual(type(Job_inventory.get_fact_expressions(self, 'Windows')), list)

    def test_count_expressions_windows(self):

        list_elements = 5
        setup_inventory_table(self)
        
        self.assertEqual(len(Job_inventory.get_fact_expressions(self, 'Windows')), list_elements)

    def test_update_db_linux(self):

        setup_inventory_table(self)

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
            'system', 
            ]

        
        for test in range(len(expressions)):
            match_value = value_match([match[match_count]])
            print(match_value[0].value)
            match_count += 1

            #Job_inventory.update_inventory_db(self, match, system, host, expressions[test])

if __name__ == '__main__':
    unittest.main()