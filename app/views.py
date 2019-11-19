import requests
import json
import time

from django.shortcuts import render
from django.http import HttpResponse

championsURL= "http://ddragon.leagueoflegends.com/cdn/9.3.1/data/en_US/champion.json"
championImageURL = "http://ddragon.leagueoflegends.com/cdn/9.22.1/img/champion/" #name.png
#champions = []


# home page should display some interesting analytics
def home(request):
    context = {}
    query = ""
    if request.GET:
        query = request.GET['q']
        context['query'] = str(query)

    return render(request, 'LolWin/home.html', context)

def about(request):
    return render(request, 'LolWin/about.html')

def champions(request):
    champions = getChampions()
    context = {'champions': champions}
    return render(request, 'LolWin/champion.html', context)

def getChampions():
    champions = []
    championData = requests.get(championsURL).json()
    for champId in championData['data'].keys():
        champName = championData['data'][champId]['name']
        champions.append({"name": champName, "id": champId})

    return champions