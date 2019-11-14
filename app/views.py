from django.shortcuts import render
from django.http import HttpResponse

def home(request):

    context = {}

    query = ""
    if request.GET:
        query = request.GET['q']
        context['query'] = str(query)

    return render(request, 'LolWin/home.html', context)

def about(request):
    return render(request, 'LolWin/about.html')