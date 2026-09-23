# Create your models here.
# Create your models here.

from django.db import models


class Pays(models.Model):
    nom = models.CharField(max_length=200)
    tva = models.FloatField()
    tarif_electrique = models.FloatField()
    salaire_minimum = models.FloatField()


class Ville(models.Model):
    nom = models.CharField(max_length=200)
    taxe_immobiliere = models.FloatField()
    prix_m2 = models.FloatField()
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE)


class Machine(models.Model):
    nom = models.CharField(max_length=200)
    prix = models.FloatField()
    duree_de_vie = models.FloatField()
    cout_maintenance = models.FloatField()
    superficie = models.FloatField()


class QuantiteMachine(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    nombre = models.IntegerField()


class Lieu(models.Model):
    nom = models.CharField(max_length=200)
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE)
    superficie = models.FloatField()
    quantite_machine = models.ManyToManyField(QuantiteMachine)
    consommation_electrique = models.FloatField()


class Transport(models.Model):
    nombre_palettes = models.IntegerField()
    cout = models.FloatField()
    delai = models.FloatField()
    depart = models.FloatField()
    arrivee = models.FloatField()


class Produit(models.Model):
    nom = models.CharField(max_length=200)
    prix_de_vente = models.FloatField()
    duree_de_vie = models.FloatField()
    nombre_par_palette = models.IntegerField()
    operations = models.ForeignKey(Operation, on_delete=models.CASCADE)


class PrixProduit(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    prix_achat = models.FloatField()


class Fournisseur(models.Model):
    nom = models.CharField(max_length=200)
    prix_produits = models.ForeignKey(PrixProduit, on_delete=models.CASCADE)


class QuantiteProduit(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    nombre = models.IntegerField()


class Stock(models.Model):
    quantite_produits = models.ManyToManyField(QuantiteProduit)
    palettes_max = models.IntegerField()


class PointDeVente(models.Model):
    nom = models.CharField(max_length=200)
    lieu = models.ForeignKey(Lieu, on_delete=models.CASCADE)
    heures_de_travail = models.FloatField()
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)


class Facture(models.Model):
    quantite_produits = models.ManyToManyField(QuantiteProduit)
    reduction = models.FloatField()
    point_de_vente = models.ForeignKey(PointDeVente, on_delete=models.CASCADE)
    client = models.CharField(max_length=200)


class Operation(models.Model):
    nom = models.CharField(max_length=200)
    operation_suivante = models.ForeignKey("self", on_delete=models.CASCADE)
    cout = models.FloatField()
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    quantite_produits = models.ManyToManyField(QuantiteProduit)
    heures_de_travail = models.FloatField()
    consommation_electrique = models.FloatField()
