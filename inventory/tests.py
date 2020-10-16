from django.test import TestCase
import unittest
from inventory.models import Inventory
from inventory.jobs.minutely.update_inventory_table import Job
class TestInventoryValues(TestCase):


    def test_get_host(self):
        """
        docstring
        """
        a = 1
        b = 2

        c = a + b

        self.assertEqual(c, 3)


if __name__ == '__main__':
    unittest.main()