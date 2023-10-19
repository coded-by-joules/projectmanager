from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainpage, name="projectall"),
    path('new', views.newproject, name="newproject"),
    path('<project_ord>/', views.projectview, name="project"),
    path('edit/<project_code>', views.projectedit, name="projectedit"),
    path('delete/<project_code>', views.projectdel, name="projectdel")
]
