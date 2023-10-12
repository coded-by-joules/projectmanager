from django.db import models
import string
import random

# Generate random slug
def generate_unique_code():
    length = 6

    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Project.objects.filter(code=code).count() == 0:
            break

    return code


# Create your models here.
class Project(models.Model):
    STATUS_CHOICES = [
     ("Headsup","Headsup"),
     ("Programming","Programming"),
     ("Changes","Changes"),
     ("Live", "Live"),
     ("Closed", "Closed")
    ]
    REGION_CHOICES = [
      ("APAC","APAC"),
      ("EMEA","EMEA"),
      ("NA","NA")
    ]
    PLATFORM_CHOICES = [
      ("Decipher", "Decipher"),
      ("CMIX","CMIX"),
      ("Confirmit","Confirmit")
    ]
        
    code = models.SlugField(max_length=8, default=generate_unique_code, unique=True)
    ord = models.CharField(max_length=15, unique=True)
    project_name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, default="Headsup", choices=STATUS_CHOICES)
    created_date = models.DateField(auto_now_add=True)
    region = models.CharField(max_length=10, blank=True, choices=REGION_CHOICES)
    pid = models.CharField(max_length=20, blank=True)
    platform = models.CharField(max_length=15, default="Decipher", choices=PLATFORM_CHOICES)
    markets = models.CharField(max_length=50, blank=True)
    hours = models.CharField(max_length=20, blank=True)
    eta = models.DateTimeField()
    
    def __str__(self):
        return f"{self.ord} - {self.project_name}"
