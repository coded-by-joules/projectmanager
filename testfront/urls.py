from django.urls import path
from .views import mainpage, projectview, newproject

urlpatterns = [
    path('', mainpage, name="projectall"),
    path('project/new', newproject, name="newproject"),
    path('project/<project_ord>', projectview, name="project"),
]
