from django.db import models


# Create your models here.
class RegularPizza(models.Model):
    name = models.CharField(max_length=64)
    max_price = models.FloatField()
    min_price = models.FloatField()

class SicilianPizza(models.Model):
    name = models.CharField(max_length=64)
    max_price = models.FloatField()
    min_price = models.FloatField()


class Toppings(models.Model):
    name = models.CharField(max_length=64)


class Subs(models.Model):
    name = models.CharField(max_length=64)
    max_price = models.FloatField()
    min_price = models.FloatField()


class SubsExtras(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()


class Pasta(models.Model):
    name = models.CharField(max_length=64)
    max_price = models.FloatField()
    min_price = models.FloatField()

class Salads(models.Model):
    name = models.CharField(max_length=64)
    max_price = models.FloatField()
    min_price = models.FloatField()


class DinnerPlatters(models.Model):
    name = models.CharField(max_length=64)
    max_price = models.FloatField()
    min_price = models.FloatField()
