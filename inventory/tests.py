from django.test import TestCase
import unittest
from inventory.models import Inventory
from hosts.models import hosts
from inventory.jobs.minutely.update_inventory_table import Job as Job_update
from inventory.jobs.hourly.update_inventory import Job as Job_inventory


def setup_inventory_table(classArg, host='localhost', ):
    hosts.objects.create(hostname = host)
    return Job_update.execute(classArg)

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
    
    def test_get_expressions(self):
        """
        docstring
        """

        setup_inventory_table(self)
        self.assertEqual(type(Job_inventory.get_fact_expressions(self, 'Linux')), list)

    def test_count_expressions(self):

        list_elements = 6
        setup_inventory_table(self)
        
        self.assertEqual(len(Job_inventory.get_fact_expressions(self, 'Linux')), list_elements)

if __name__ == '__main__':
    unittest.main()