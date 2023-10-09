from django.shortcuts import render
from rest_framework import generics
from .serializers import ProjectSerializer
from .models import Project

# Create your views here.
class ProjectView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer