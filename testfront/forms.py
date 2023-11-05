from django import forms
from api.models import Project, ProjectLog
from datetime import datetime, timedelta

class ProjectForm(forms.ModelForm):
    class Meta:
       form_controlClass = {"class": "form-control"}
       form_selectClass = {"class": "form-select"}
       eta = datetime.today() + timedelta(hours=1)
       etastr = eta.strftime("%Y-%m-%dT%H:00")

       model = Project
       fields = "__all__"
       exclude = ["code","creator","status"]
       widgets = {
           "ord": forms.TextInput(attrs={**form_controlClass, "placeholder":"ORD-XXXXXX-XXXX"}),
           "project_name": forms.TextInput(attrs=form_controlClass),
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

class ProjectLogForm(forms.ModelForm):
    class Meta:
       model = ProjectLog
       fields = ["id","message", "update_type"]
       widgets = {
            "message": forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter your update here", "rows":"5"}),
            "update_type": forms.Select(attrs={"class":"form-select form-select-sm"})
        }

    def __init__(self, *args, **kwargs):
        project = kwargs.pop("project", None)        
        super().__init__(*args, **kwargs)
        if isinstance(project, Project):
            if project.status in ["Headsup"]:
                self.fields["update_type"].choices = [
                    ('update', 'Update only'),
                    ('scripting', 'Started Scripting'),
                    ("toclosed","Set to Closed")
                ]
            elif project.status in ["Programming"]:
                self.fields["update_type"].choices = [
                    ('update', 'Update only'),
                    ("testlinksent","Test Link Sent"),                    
                    ("settolive","Set to Live"),
                    ("paused","Paused"),
                    ("toclosed","Set to Closed")
                ]
            elif project.status in ["Changes"]:
                self.fields["update_type"].choices = [
                    ('update', 'Update only'),
                    ("settolive","Set to Live"),
                    ("paused","Paused"),
                    ("toclosed","Set to Closed")
                ]
            elif project.status in ["Live"]:
                self.fields["update_type"].choices = [
                    ('update', 'Update only'),
                    ("settolivechange","Change to Live Changes"),
                    ("paused","Paused"),
                    ("toclosed","Set to Closed")
                ]
            elif project.status in ["LiveChange"]:
                self.fields["update_type"].choices = [
                    ('update', 'Update only'),
                    ("settolive","Set to Live"),
                    ("paused","Paused"),
                    ("toclosed","Set to Closed")
                ]
            elif project.status in ["Paused"]:
                self.fields["update_type"].choices = [
                    ('update', 'Update only'),
                    ("settolive","Set to Live"),
                    ("toclosed","Set to Closed")
                ]
            elif project.status in ["Closed"]:
                self.fields["update_type"].choices = [
                    ('update', 'Update only'),
                    ("reopened","Re-open Project"),
                ]