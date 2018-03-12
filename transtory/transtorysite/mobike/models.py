# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class BikeType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    codename = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bike_types'


class BikeSubtype(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True, verbose_name="Bike type")
    type = models.ForeignKey(BikeType, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bike_subtypes'


class Bike(models.Model):
    id = models.IntegerField(primary_key=True)
    sn = models.TextField(blank=True, null=True, verbose_name="Bike SN")
    subtype = models.ForeignKey(BikeSubtype, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bikes'


class BikeService(models.Model):
    id = models.IntegerField(primary_key=True)
    bike = models.ForeignKey(Bike, models.DO_NOTHING, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bike_services'


class Trip(models.Model):
    id = models.IntegerField(primary_key=True)
    # bike_service = models.ForeignKey(BikeService, models.DO_NOTHING, blank=True, null=True)
    bike_service = models.OneToOneField(BikeService, models.DO_NOTHING)
    city = models.TextField(blank=True, null=True)
    time = models.TextField(blank=True, null=True)
    departure_region = models.TextField(blank=True, null=True)
    departure_place = models.TextField(blank=True, null=True)
    departure_coordinate = models.TextField(blank=True, null=True)
    arrival_region = models.TextField(blank=True, null=True)
    arrival_place = models.TextField(blank=True, null=True)
    arrival_coordinate = models.TextField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    distance = models.TextField(blank=True, null=True)  # This field type is a guess.
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trips'
