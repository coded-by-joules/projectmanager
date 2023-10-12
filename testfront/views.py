from django.shortcuts import render, redirect
from api.models import Project
from .forms import ProjectForm
from django.contrib import messages


# Create your views here.
def mainpage(request):
    projects = Project.objects.all()
    return render(request, "testfront/projectlist.html", {
        "projects": projects,
        "count": len(projects)
    })

def projectview(request, project_ord):
    project = Project.objects.get(ord=project_ord)
    return render(request, "testfront/project.html", {
        "project": project
    })

def newproject(request):
    if request.method == "GET":            
       form = ProjectForm()           
       return render(request, "testfront/formproject.html", {
           "form": form
       })
    else:
       form = ProjectForm(request.POST)
       if form.is_valid():
           project = Project(
               ord = form.cleaned_data["ord"],
               project_name = form.cleaned_data["project_name"],
               status = form.cleaned_data["status"],
               region = form.cleaned_data["region"],
               pid = form.cleaned_data["pid"],
               platform = form.cleaned_data["platform"],
               markets = form.cleaned_data["markets"],
               hours = form.cleaned_data["hours"],
               eta = form.cleaned_data["eta"]
           )
           project.save()
           messages.success(request, "Project added succesfully")

           return redirect("/")
       else:
           print("Form is invalid")
           return render(request, "testfront/formproject.html", {
            "form": form
           })
