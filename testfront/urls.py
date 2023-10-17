from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainpage, name="projectall"),
    path('project/new', views.newproject, name="newproject"),
    path('project/<project_ord>', views.projectview, name="project"),
    path('project/edit/<project_code>', views.projectedit, name="projectedit"),
    path('project/delete/<project_code>', views.projectdel, name="projectdel")
]
