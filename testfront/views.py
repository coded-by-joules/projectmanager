from django.shortcuts import render, redirect
from api.models import Project
from .forms import ProjectForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
import re
from django.core.paginator import Paginator

# Create your views here.
def mainpage(request):
    if "search" in request.GET:
        searchTxt = str(request.GET['search']).strip()
        if searchTxt.strip() == "":
            projects_list = Project.objects.all()
        else:
            # check if search matches ord
            try:
                if re.search("^ORD-[0-9]{6}-[0-9A-Z]{4}$", searchTxt):
                    projects_list = Project.objects.get(ord=searchTxt)
                else:
                    projects_list = Project.objects.filter(ord__icontains=searchTxt) | Project.objects.filter(project_name__icontains=searchTxt)
            except Exception:
                projects_list = [] # return empty if not found
    else:
        projects_list = Project.objects.all()

    project_pages = Paginator(projects_list, 15)
    page_num = 1
    if "page" in request.GET:
        if str(request.GET['page']).isdigit():
            page_num = int(request.GET['page'])
            if page_num > project_pages.num_pages:
                page_num =  project_pages.num_pages
    
    min_page = page_num - 2
    if min_page <= 1:
        min_page = 1
    max_page = min_page + 4
    if max_page >= project_pages.num_pages:
        max_page = project_pages.num_pages


    project_page = project_pages.page(page_num)
    
    prev_page = 1
    if project_page.has_previous():
        prev_page = page_num - 1
    next_page = project_pages.num_pages
    if project_page.has_next():
        next_page = page_num + 1
        
    return render(request, "testfront/projectlist.html", {
        "projects": project_page.object_list,
        "pages": range(min_page, max_page+1),
        "last": project_pages.num_pages,
        "current": project_page.number,
        "showPrev": project_page.has_previous(),
        "showNext": project_page.has_next(),
        "prev_page": prev_page,
        "next_page": next_page
    })
    
    

def projectview(request, project_ord):
    project = get_object_or_404(Project, ord=project_ord)
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

def projectedit(request, project_code):    
    editproj =get_object_or_404(Project, code=project_code)
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

def projectdel(request, project_code):    
    project = get_object_or_404(Project, code=project_code)
    if (request.method == "GET"):
        return render(request, "testfront/formdelete.html", {
            "project": project
        })
    else:
        project.delete()
        return redirect("projectall")