from django.db import models

# Create your models here.
class Project(models.Model):
    ord = models.CharField(max_length=15, unique=True)
    project_name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, default="Headsup")
    created_date = models.DateField(auto_now_add=True)
    region = models.CharField(max_length=10, blank=True)
    pid = models.CharField(max_length=20, blank=True)
    markets = models.CharField(max_length=50, blank=True)
    hours = models.CharField(max_length=20, blank=True)
    eta = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.ord} - {self.project_name}"
