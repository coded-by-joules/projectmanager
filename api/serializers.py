from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id','code','ord','project_name','status','platform','created_date','region','pid','markets','hours','eta')