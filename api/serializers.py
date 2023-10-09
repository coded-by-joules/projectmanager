from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id','ord','project_name','status','created_date','region','pid','markets','hours','eta')