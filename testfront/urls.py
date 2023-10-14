from django.urls import path
from . views import mainpage, newproject, projectview, projectedit

urlpatterns = [
    path('', mainpage, name="projectall"),
    path('project/new', newproject, name="newproject"),
    path('project/<project_ord>', projectview, name="project"),
    path('project/edit/<project_ord>', projectedit, name="projectedit")
]
