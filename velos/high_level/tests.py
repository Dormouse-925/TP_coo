
# high_level/tests.py
from django.test import TestCase
from .models import Pays, Ville, Lieu, Machine, QuantiteMachine

class MachineModelTests(TestCase):
    def test_machine_creation(self):
        self.assertEqual(Machine.objects.count(), 0)
        Machine.objects.create(nom="CNC", prix=3000, duree_de_vie=100, cout_maintenance=18, superficie=8 )
        self.assertEqual(Machine.objects.count(), 1)
     

class MachineCostsTests(TestCase):
    def test_machine_creation(self):
    
        machine = Machine.objects.create(nom="Machine test", prix=3000, duree_de_vie=100, cout_maintenance=18, superficie=8 )
        self.assertEqual(machine.costs(), 48)

class MachineCostsTests(TestCase):
    def test_machine_creation(self):
    
        machine = Machine.objects.create(nom="Machine test", prix=3000, duree_de_vie=100, cout_maintenance=18, superficie=8 )
        self.assertEqual(machine.costs(), 48)

class LieuCostsTest(TestCase):

    def test_cout_lieu(self):
        
        france = Pays.objects.create(nom="France", tva=20, tarif_electrique=0.2, salaire_minimum=12 )
        labege = Ville.objects.create(nom="Labège", taxe_immobiliere=0, prix_m2=2000, pays=france
        )

        machine1 = Machine.objects.create(nom="Machine 1", prix=10000, duree_de_vie=1, cout_maintenance=0, superficie=0)
        machine2 = Machine.objects.create(nom="Machine 2", prix=5000, duree_de_vie=1, cout_maintenance=0, superficie=0)

        quantite_machine1 = QuantiteMachine.objects.create(machine=machine1, nombre=1)
    
        quantite_machine2 = QuantiteMachine.objects.create(machine=machine2, nombre=1)
        
        lieu = Lieu.objects.create(nom="Lieu de production", ville=labege, superficie=50, consommation_electrique=5000)
        
        lieu.quantite_machine.add(quantite_machine1, quantite_machine2)
        self.assertEqual(lieu.costs(), 116000)