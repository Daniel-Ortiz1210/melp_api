from django.db import models

class Restaurant(models.Model):
    id = models.CharField(unique=True, primary_key=True, max_length=70)
    rating = models.IntegerField()
    name = models.CharField(max_length=100)
    site = models.URLField(max_length=300)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.name

