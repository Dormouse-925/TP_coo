# Create your models here.
# Create your models here.

from django.db import models


class Pays(models.Model):
    nom = models.CharField(max_length=200)
    tva = models.FloatField()
    tarif_electrique = models.FloatField()
    salaire_minimum = models.FloatField()
    def _str_(self):
        return self.nom
 
    def costs(self):
        return self.tarif_electrique + self.salaire_minimum


class Ville(models.Model):
    nom = models.CharField(max_length=200)
    taxe_immobiliere = models.FloatField()
    prix_m2 = models.FloatField()
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE)
    def _str_(self):
        return self.nom
    
    def costs(self):
        return self.prix_m2


class Machine(models.Model):
    nom = models.CharField(max_length=200)
    prix = models.FloatField()
    duree_de_vie = models.FloatField()
    cout_maintenance = models.FloatField()
    superficie = models.FloatField()
    def _str_(self):
        return self.nom

    def costs(self):

        if self.duree_de_vie <= 0:
            return self.cout_maintenance

        return (self.prix / self.duree_de_vie) + self.cout_maintenance



class QuantiteMachine(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    nombre = models.IntegerField()
    def _str_(self):
        return f"{self.machine.nom} {self.nombre}"


class Lieu(models.Model):
    nom = models.CharField(max_length=200)
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE)
    superficie = models.FloatField()
    quantite_machine = models.ManyToManyField(QuantiteMachine)
    consommation_electrique = models.FloatField()
    def _str_(self):
        return self.nom

    def costs(self):
        
        cout_immobilier = self.superficie * self.ville.prix_m2

        cout_electricite = (
            self.consommation_electrique * self.ville.pays.tarif_electrique
        )

        cout_machines = sum(
            quantite.costs()
            for quantite in self.quantite_machine.all()
        )

        return cout_immobilier + cout_electricite + cout_machines


class Transport(models.Model):
    nombre_palettes = models.IntegerField()
    cout = models.FloatField()
    delai = models.FloatField()
    depart = models.FloatField()
    arrivee = models.FloatField()
    def _str_(self):
        return f"{self.nombre_palettes} {self.depart} {self.arrivee}"

    def costs(self):
        return self.cout

class Produit(models.Model):
    nom = models.CharField(max_length=200)
    prix_de_vente = models.FloatField()
    duree_de_vie = models.FloatField()
    nombre_par_palette = models.IntegerField()
    operations = models.ForeignKey("Operation", on_delete=models.CASCADE, blank = True, null = True)
    def _str_(self):
        return self.nom 


    def costs(self):

        if self.operations is None:
            return 0

        cout_total = 0
        operation = self.operations

        while operation is not None:
            cout_total += operation.costs()
            operation = operation.operation_suivante

        return cout_total

class PrixProduit(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    prix_achat = models.FloatField()
    def _str_(self):
        return f"{self.produit.nom} {self.prix_achat}"


class Fournisseur(models.Model):
    nom = models.CharField(max_length=200)
    prix_produits = models.ForeignKey(PrixProduit, on_delete=models.CASCADE)
    def _str_(self):
        return f"{self.nom} {self.prix_produits.produit.nom} {self.prix_produits.prix_achat}"


class QuantiteProduit(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    nombre = models.IntegerField()
    def _str_(self):
        return f"{self.produit.nom} {self.nombre}"

    def costs(self):
        return self.nombre *self.produit.costs()


class Stock(models.Model):
    quantite_produits = models.ManyToManyField(QuantiteProduit)
    palettes_max = models.IntegerField()
    def _str_(self):
        return f"{self.palettes_max}"

    def costs(self):
        return sum(
            quantite.costs()
            for quantite in self.quantite_produits.all()
        )

class PointDeVente(models.Model):
    nom = models.CharField(max_length=200)
    lieu = models.ForeignKey(Lieu, on_delete=models.CASCADE)
    heures_de_travail = models.FloatField()
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    def _str_(self):
        return f"{self.nom} {self.lieu.nom}"

    def costs(self):

        cout_MO = (
            self.heures_de_travail * self.lieu.ville.pays.salaire_minimum
        )
        return self.lieu.couts() + self.stock.couts() + cout_MO


class Facture(models.Model):
    quantite_produits = models.ManyToManyField(QuantiteProduit)
    reduction = models.FloatField()
    point_de_vente = models.ForeignKey(PointDeVente, on_delete=models.CASCADE)
    client = models.CharField(max_length=200)
    def _str_(self):
        return f"{self.point_de_vente.nom} {self.lieu.nom} {self.client}"


class Operation(models.Model):
    nom = models.CharField(max_length=200)
    operation_suivante = models.ForeignKey("self", on_delete=models.CASCADE, blank = True, null =True)
    cout = models.FloatField()
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    quantite_produits = models.ManyToManyField(QuantiteProduit)
    heures_de_travail = models.FloatField()
    consommation_electrique = models.FloatField()
    def _str_(self):
        return f"{self.nom} {self.Machine.nom} {self.heures_de_travail}"

    def costs(self):
      
        cout_machine = (
            self.machine.costs() * self.heures_de_travail
        )

        return cout_machine + self.cout
    