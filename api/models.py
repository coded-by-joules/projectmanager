from django.db import models
import string
import random
import pytz
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.urls import reverse

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
     ("LiveChange", "Live Changes"),
     ("Paused", "Paused"),
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
    # eta check
    __original_eta = None

    code = models.SlugField(max_length=8, default=generate_unique_code, unique=True)
    ord = models.CharField(max_length=15, unique=True, validators=[RegexValidator(regex="^ORD-[0-9]{6}-[0-9A-Z]{4}$", message="Please enter the ORD in ORD-XXXXX-XXXX format.")])
    project_name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, default="Headsup", choices=STATUS_CHOICES)
    created_date = models.DateField(auto_now_add=True)
    region = models.CharField(max_length=10, blank=True, choices=REGION_CHOICES)
    pid = models.CharField(max_length=20, blank=True)
    platform = models.CharField(max_length=15, default="Decipher", choices=PLATFORM_CHOICES)
    eta = models.DateTimeField(null=True,blank=True)
    details = models.TextField(max_length=255, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_eta = self.eta

    # validation to check ETA
    def clean(self):
      if self.eta is not None:
        data = datetime.strptime(str(self.eta), "%Y-%m-%d %H:%M:%S%z")
        nowdata = datetime.now() + timedelta(hours=1)
        now = pytz.utc.localize(nowdata)

        if (now > data):
            if self.__original_eta is not None:
              if self.eta != self.__original_eta:
                raise ValidationError({
                  "eta": "If you wish to change the ETA, please enter an ETA at least an hour from now"
                })
            else:
              raise ValidationError({
                 "eta": "Please enter an ETA at least an hour from today"
              })    

    def __str__(self):
        return f"{self.ord} - {self.project_name}"
    
    def get_absolute_url(self):        
        return reverse("project", args=[self.ord])    

class ProjectLog(models.Model):
   UPDATE_CHOICES = [
      ("update","Update only"),
      ("scripting","Started Scripting"),
      ("testlinksent","Test Link Sent"),
      ("settolive","Set to Live"),
      ("settolivechange","Change to Live Changes"),
      ("paused","Paused"),
      ("toclosed","Set to Closed"),
      ("reopened","Re-open Project"),
      ("created","Project created"),
      ("edited","Project details edited")
   ]

   HEADER_CHOICES = [
      ("update","posted an update"),
      ("scripting","started scripting the project"),
      ("testlinksent","sent the test link(s)"),
      ("settolive","launched the study"),
      ("settolivechange","made some live changes"),
      ("paused","paused the study"),
      ("toclosed","closed the study"),
      ("reopened","reopened the study"),
      ("created","created this project"),
      ("edited","edited some details for this project")      
   ]

   project = models.ForeignKey(Project, on_delete=models.CASCADE, to_field="code")
   creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
   log_header = models.CharField(max_length=255, default="update", choices=HEADER_CHOICES)
   message = models.TextField(max_length=255, blank=True, null=True)   
   update_type = models.CharField(max_length=20, default="update", choices=UPDATE_CHOICES)
   created = models.DateTimeField(auto_now_add=True)