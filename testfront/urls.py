from django.urls import path
from . views import mainpage, projectview

urlpatterns = [
    path('', mainpage, name="projectall"),
    path('project/<project_ord>', projectview, name="project")
]
