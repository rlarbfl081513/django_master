from django.db import models

# Create your models here.
class Artists(models.Model):
  name = models.TextField(max_length=100)
  agency = models.TextField()
  debut_data = models.DateField()
  is_group = models.BooleanField()