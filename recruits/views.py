from django.shortcuts import render
from .models import Recruit

def job_list(request):
    recruits = Recruit.objects.all()

    context = {'recruits' : recruits}
    return render(request, 'job_list.html', context)