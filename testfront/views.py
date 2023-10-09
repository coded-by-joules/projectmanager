from django.shortcuts import render
from api.models import Project
from urllib.parse import unquote

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