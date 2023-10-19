from django.db import models
from django.contrib.auth.models import User

# Create your models here.

POSITION_CHOICES = [
     ("SP","Survey Programmer"),
     ("DP","Data Processor"),
     ("PM","Project Manager"),
     ("QA", "Quality Assurance")
]

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=30, choices=POSITION_CHOICES)
