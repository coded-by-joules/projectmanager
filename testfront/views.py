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
           form.save()
           messages.success(request, "Project added succesfully")
           return redirect("projects/")
       else:
           print("Form is invalid")
           return render(request, "testfront/formproject.html", {
            "form": form
           })

def projectedit(request, project_ord):
    return render(request, "testfront/formproject.html")