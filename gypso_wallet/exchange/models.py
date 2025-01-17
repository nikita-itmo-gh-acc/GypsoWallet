from django.db import models

# Create your models here.
class Token(models.Model):
    price = models.CharField(max_length = 20)