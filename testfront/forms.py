from django import forms
from api.models import Project
from datetime import datetime, timedelta

class ProjectForm(forms.ModelForm):
    class Meta:
       form_controlClass = {"class": "form-control"}
       form_selectClass = {"class": "form-select"}
       eta = datetime.today() + timedelta(hours=1)
       etastr = eta.strftime("%Y-%m-%dT%H:00")

       model = Project
       fields = "__all__"
       exclude = ["code","creator"]
       widgets = {
           "ord": forms.TextInput(attrs={**form_controlClass, "placeholder":"ORD-XXXXXX-XXXX"}),
           "project_name": forms.TextInput(attrs=form_controlClass),
           "status": forms.Select(attrs=form_selectClass),
           "region": forms.Select(attrs=form_selectClass),
           "pid": forms.TextInput(attrs={**form_controlClass, "placeholder":"Example, for Decipher projects, ID is 53c/201104"}),
           "platform": forms.Select(attrs=form_selectClass),
           "hours": forms.TextInput(attrs=form_controlClass),
           "eta": forms.TextInput(attrs={**form_controlClass, "type":"datetime-local", "min":etastr}),
           "details": forms.Textarea(attrs=form_controlClass)
       }
    
    def __init__(self, *args, **kwargs):
        method = kwargs.pop("method", "add")
        super().__init__(*args,**kwargs)
        if (method == "edit"):
            self.fields["ord"].disabled = True
            self.fields["status"].disabled = True 