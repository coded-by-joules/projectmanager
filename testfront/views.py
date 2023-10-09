from django.shortcuts import render
from api.models import Project

# Create your views here.
def mainpage(request):
    projects = Project.objects.all()
    return render(request, "testfront/index.html", {
        "projects": projects
    })