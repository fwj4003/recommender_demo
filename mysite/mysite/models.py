# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class AllDrama(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=20, blank=True)
    url = models.CharField(max_length=100, blank=True)
    cover = models.CharField(max_length=100, blank=True)
    rate = models.CharField(max_length=5, blank=True)

    class Meta:
        managed = False
        db_table = 'all_drama'


class Contents(models.Model):
    no = models.IntegerField(primary_key=True)
    id = models.CharField(max_length=10)
    title = models.CharField(max_length=50, blank=True)
    year = models.CharField(max_length=10, blank=True)
    score = models.CharField(max_length=5, blank=True)
    director = models.CharField(max_length=50, blank=True)
    classification = models.CharField(max_length=20, blank=True)
    actor = models.CharField(max_length=100, blank=True)
    feature = models.CharField(max_length=160, blank=True)

    class Meta:
        managed = False
        db_table = 'contents'


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'

class Rates(models.Model):
    no = models.IntegerField(primary_key=True)
    aid = models.CharField(max_length=20)
    score = models.CharField(max_length=500, blank=True)

    class Meta:
        managed = False
        db_table = 'rates'


class Todo(models.Model):
    id = models.BigIntegerField(primary_key=True)
    title = models.TextField(blank=True)
    created = models.DateTimeField()
    done = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'todo'