from django.db import models


class Zip(models.Model):
    zip = models.CharField(max_length=10, blank=True, default="")

    def __str__(self):
        return self.zip


class City(models.Model):
    city = models.CharField(max_length=50, blank=True, default="")

    def __str__(self):
        return self.city
