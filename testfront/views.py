from django.shortcuts import render, redirect
from api.models import Project, ProjectLog
from .forms import ProjectForm, ProjectLogForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
import re
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User

# search project setup
def search_project(search_key):
    searchTxt = search_key.strip()
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
    
    return projects_list

# paginator setup
def paginator_setup(projects_list: Project, page_get):
    project_pages = Paginator(projects_list.order_by("created_date"), 15)
    page_num = page_get

    if page_num >= project_pages.num_pages:
        page_num = project_pages.num_pages
    
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

    return {
        "projects": project_page.object_list,
        "pages": range(min_page, max_page+1),
        "last": project_pages.num_pages,
        "current": project_page.number,
        "showPrev": project_page.has_previous(),
        "showNext": project_page.has_next(),
        "prev_page": prev_page,
        "next_page": next_page
    }

def addtolog(projectObj: Project, user: User, updates=""):
    logCheck = ProjectLog.objects.filter(project=projectObj).count()
    if logCheck > 0:
        log = ProjectLog(
            project=projectObj,
            creator=user,
            update_type="edited",
            message=f"{user.first_name} {user.last_name} edited the {updates} details for this project"
        )
    else:
        log = ProjectLog(
            project=projectObj,
            creator=user,
            update_type="created",
            message=f"{user.first_name} {user.last_name} created this project."
        )
    
    log.save()
        

# Create your views here.
@login_required
def mainpage(request):
    if "search" in request.GET:
        projects_list = search_project(request.GET["search"])
    else:
        projects_list = Project.objects.all()

    page_num = 1
    if "page" in request.GET:
        if str(request.GET["page"]).isdigit():
            page_num = int(request.GET["page"])

    paginator_result = paginator_setup(projects_list, page_num)        
    return render(request, "testfront/projectlist.html", paginator_result)

@login_required
@permission_required("api.view_project",raise_exception=True)
def projectview(request, project_ord):
    project = get_object_or_404(Project, ord=project_ord)
    creator = f"{project.creator.first_name} {project.creator.last_name}"
    logs = ProjectLog.objects.filter(project=project).order_by("-created")

    if request.method == "GET":
        logform = ProjectLogForm()

    return render(request, "testfront/project.html", {
        "project": project,
        "creator": creator,
        "form": logform,
        "logs": logs
    })

@login_required
@permission_required("api.add_project",raise_exception=True)
def newproject(request):
    if request.method == "GET":            
       form = ProjectForm(initial={'creator':request.user.username})           
       return render(request, "testfront/formproject.html", {
           "form": form,           
           "formText": "Add"
       })
    else:
       form = ProjectForm(request.POST)
       if form.is_valid():
           project = form.save(commit=False)
           project.creator = request.user
           project.save()

           addtolog(project, request.user)
           messages.success(request, "Project added succesfully")
           return redirect("projectall")
       else:
           print("Form is invalid")
           return render(request, "testfront/formproject.html", {
            "form": form,
            "formText": "Add"
           })

@login_required
def projectedit(request, project_code):
    editproj = get_object_or_404(Project, code=project_code)
    if (editproj.creator != request.user and not request.user.has_perm("api.change_project")):
        return HttpResponseForbidden("Access denied")
    
    if request.method == "GET":
        username = f"{editproj.creator.first_name} {editproj.creator.last_name}"
        form = ProjectForm(instance = editproj, method="edit")
        return render(request, "testfront/formproject.html", {
            "form": form,
            "formText": "Edit",
            "username": username
        })
    else:
        form = ProjectForm(request.POST, instance=editproj, method="edit")
        if form.is_valid():
            updates = ""
            if form.has_changed():
                updates = ", ".join(form.changed_data)
            project = form.save()

            addtolog(project, request.user, updates)
            messages.success(request, "Project edited successfully")
            return redirect("projectall")
        else:
            print("Form is invalid")
            return render(request, "testfront/formproject.html", {
            "form": form,
            "formText": "Edit"
           })

@login_required
def projectdel(request, project_code):    
    project = get_object_or_404(Project, code=project_code)
    if (project.creator != request.user and not request.user.has_perm("api.change_project")):
        return HttpResponseForbidden("Access denied")

    if (request.method == "GET"):
        return render(request, "testfront/formdelete.html", {
            "project": project
        })
    else:
        project.delete()
        return redirect("projectall")