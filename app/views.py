from django.shortcuts import render
from django.http import HttpResponse

def home(request):

    context = {}

    # this query is the search for the summoner name. This function servers as the root for all logic involving analytics.
    # the search will gather your stats for games using that champ and train itself using generalized stats and comparing
    # the results to your games.
    query = ""
    if request.GET:
        query = request.GET['q']
        context['query'] = str(query)

    return render(request, 'LolWin/home.html', context)

def about(request):
    return render(request, 'LolWin/about.html')