from django.shortcuts import render
from .models import Recruit

def job_list(request):
    recruits = Recruit.objects.all()
    context = {'recruits' : recruits}
    return render(request, 'job_list.html', context)

def job_table(request):
    recruits = Recruit.objects.all()
    context = {'recruits' : recruits}
    return render(request, 'job_table.html', context)

def job_graph(request):
    recruits = Recruit.objects.all()
    context = {'recruits' : recruits}
    return render(request, 'job_graph.html', context)