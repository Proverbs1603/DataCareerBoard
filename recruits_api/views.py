from django.shortcuts import render
from rest_framework import generics
from recruits_api.serializers import RecruitSerializer
from recruits.models import Recruit

class RecruitList(generics.ListCreateAPIView):
    queryset = Recruit.objects.all()
    serializer_class = RecruitSerializer