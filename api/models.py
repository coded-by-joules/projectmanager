from django.db import models
import string
import random
import pytz
import re
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from django.core.validators import RegexValidator

# Generate random slug
def generate_unique_code():
    length = 6

    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Project.objects.filter(code=code).count() == 0:
            break

    return code

# eta validator
def validate_eta(value):
   if value not in ["",None]:
        data = datetime.strptime(str(value), "%Y-%m-%d %H:%M:%S%z")
        nowdata = datetime.now() + timedelta(hours=1)
        now = pytz.utc.localize(nowdata)   

        if (now > data):
           raise ValidationError("Please enter an ETA at least an hour from today")   

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
    ord = models.CharField(max_length=15, unique=True, validators=[RegexValidator(regex="^ORD-[0-9]{6}-[0-9A-Z]{4}$", message="Please enter the ORD in ORD-XXXXX-XXXX format.")])
    project_name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, default="Headsup", choices=STATUS_CHOICES)
    created_date = models.DateField(auto_now_add=True)
    region = models.CharField(max_length=10, blank=True, choices=REGION_CHOICES)
    pid = models.CharField(max_length=20, blank=True)
    platform = models.CharField(max_length=15, default="Decipher", choices=PLATFORM_CHOICES)
    eta = models.DateTimeField(blank=True,validators=[validate_eta])
    details = models.TextField(max_length=255, blank=True)
    
    def __str__(self):
        return f"{self.ord} - {self.project_name}"