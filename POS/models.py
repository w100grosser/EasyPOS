from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField


# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=200, unique=True)
    add_date = models.DateTimeField('date added')
    price = models.FloatField()
    bar = models.BigIntegerField(unique=True)
    stock = models.BigIntegerField(default=0)
    def __str__(self):
        return self.name
    def was_published_recently(self):
        return self.add_date >= timezone.now() - timezone.timedelta(days=1)

class sellReceipt(models.Model):
    name = models.CharField(max_length=200, unique=False)
    items = models.JSONField(default=dict(items = {"__":{"bar":0}}))
    add_date = models.DateTimeField('date added')
    amount = models.FloatField(default=0)
    #items = models.ManyToManyField(Item)
    def was_published_recently(self):
        return self.add_date >= timezone.now() - timezone.timedelta(days=1)
    def __str__(self):
            return self.name

class buyReceipt(models.Model):
    name = models.CharField(max_length=200, unique=True)
    items = models.JSONField(default=dict(items = {"__":{"bar":0}}))
    add_date = models.DateTimeField('date added')
    amount = models.FloatField(default=0)
    #items = models.ManyToManyField(Item)
    def was_published_recently(self):
        return self.add_date >= timezone.now() - timezone.timedelta(days=1)
    def __str__(self):
            return self.name
