
# high_level/tests.py
from django.test import TestCase
from .models import Machine

class MachineModelTests(TestCase):
    def test_machine_creation(self):
        self.assertEqual(Machine.objects.count(), 0)
        Machine.objects.create(nom="CNC", prix=2000, duree_de_vie=100, cout_maintenance=20, superficie=8 )
        self.assertEqual(Machine.objects.count(), 1)
     

class MachineCostsTests(TestCase):
    def test_machine_creation(self):
    
        machine = Machine.objects.create(nom="Machine test", prix=2800, duree_de_vie=100, cout_maintenance=20, superficie=8 )
        self.assertEqual(machine.costs(), 40)



