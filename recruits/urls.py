from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('table/', views.job_table, name='job_table'),
    path('graph/', views.job_graph, name='job_graph'),
]
