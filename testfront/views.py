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
           "form": form,           
           "formText": "Add"
       })
    else:
       form = ProjectForm(request.POST)
       if form.is_valid():
           form.save()
           messages.success(request, "Project added succesfully")
           return redirect("projectall")
       else:
           print("Form is invalid")
           return render(request, "testfront/formproject.html", {
            "form": form,
            "formText": "Add"
           })

def projectedit(request, project_ord):    
    editproj = Project.objects.get(ord=project_ord)
    if request.method == "GET":
        form = ProjectForm(instance = editproj, method="edit")
        return render(request, "testfront/formproject.html", {
            "form": form,
            "formText": "Edit"
        })
    else:
        form = ProjectForm(request.POST, instance=editproj, method="edit")
        if form.is_valid():
            form.save()
            messages.success(request, "Project edited successfully")
            return redirect("projectall")
        else:
            print("Form is invalid")
            return render(request, "testfront/formproject.html", {
            "form": form,
            "formText": "Edit"
           })