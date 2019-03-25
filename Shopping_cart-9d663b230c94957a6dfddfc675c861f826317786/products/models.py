# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=120)
    price = models.IntegerField()
    discountPrice = models.IntegerField(default=-1)
    poster = models.CharField(max_length=20)
    description = models.CharField(max_length=500, default="No movie description available.")


    def __str__(self):
        return self.name

