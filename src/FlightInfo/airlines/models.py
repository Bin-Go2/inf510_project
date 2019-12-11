# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class City(models.Model):
    id = models.AutoField(blank=True, null=False,primary_key=True)
    rank = models.IntegerField(blank=True, null=True)
    name_eng = models.CharField(max_length=40, blank=True, null=True)
    name_chn = models.CharField(max_length=40, blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.TextField(blank=True, null=True)  # This field type is a guess.
    latitude = models.TextField(blank=True, null=True)  # This field type is a guess.
    population = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'city'


class Flight(models.Model):
    id = models.AutoField(blank=True, null=False,primary_key=True)
    flight_name = models.CharField(max_length=60, blank=True, null=True)
    departure_city = models.CharField(max_length=60, blank=True, null=True)
    arrival_city = models.CharField(max_length=60, blank=True, null=True)
    departure_airport = models.CharField(max_length=50, blank=True, null=True)
    departure_time = models.CharField(max_length=40, blank=True, null=True)
    arrival_airport = models.CharField(max_length=50, blank=True, null=True)
    arrival_time = models.CharField(max_length=50, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'flight'


class User(models.Model):
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


