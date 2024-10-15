from django.urls import path, include
from .views import *

urlpatterns = [
    path('recruit/', RecruitList.as_view(), name='recruit-list'),
]