from django import forms
from datetime import datetime, timedelta
import pytz
import re
from django.core.exceptions import ValidationError

class ProjectForm(forms.Form):
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
    form_controlClass = {"class": "form-control"}
    eta = datetime.today() + timedelta(hours=1)
    etastr = eta.strftime("%Y-%m-%dT%H:00")

    ord = forms.CharField(max_length=15, required=True, label='ord', widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "ORD-XXXXXX-XXXX"}))
    project_name = forms.CharField(max_length=200,required=True, label='project_name', widget=forms.TextInput(attrs=form_controlClass))
    status = forms.ChoiceField(choices=STATUS_CHOICES, initial="Headsup", required=True, label='status', widget=forms.Select(attrs={"class":"form-select"}))
    region = forms.ChoiceField(choices=REGION_CHOICES, required=True, label='region', widget=forms.Select(attrs={"class":"form-select"}))
    pid = forms.CharField(max_length=20, label='pid', required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Example, for Decipher projects, ID is 53c/201104"}))
    platform = forms.ChoiceField(choices=PLATFORM_CHOICES, initial="Decipher", required=True, label='platform', widget=forms.Select(attrs={"class":"form-select"}))
    markets = forms.CharField(max_length=50, label='markets', required=False, widget=forms.TextInput(attrs=form_controlClass))
    hours = forms.CharField(max_length=20, label='hours', required=False, widget=forms.TextInput(attrs=form_controlClass))
    eta = forms.DateTimeField(required=True, label='eta', widget=forms.TextInput(attrs={"class": "form-control", "type":"datetime-local", "min":etastr}))

    def clean_ord(self):
        data = self.cleaned_data["ord"]
        if (re.search("^ORD-[0-9]{6}-[0-9A-Z]{4}$", data) == None):
            raise ValidationError("Please enter the ORD in ORD-XXXXX-XXXX format.")
        
        return data
    
    def clean_eta(self):
        data = datetime.strptime(str(self.cleaned_data["eta"]), "%Y-%m-%d %H:%M:%S%z")
        nowdata = datetime.now() + timedelta(hours=1)
        now = pytz.utc.localize(nowdata)

        if (now > data):
            raise ValidationError("Please enter an ETA at least an hour from today")

        return data
