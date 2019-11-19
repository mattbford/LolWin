import requests
import json
import datetime

class champion:
    def __init__(self, name, picks, bans, wins, losses):
        self.name = name
        self.picks = picks
        self.bans = bans
        self.wins = wins
        self.losses = losses
    def __str__(self):
        return self.name + " picks: " + str(self.picks) + " bans: " + str(self.bans) + " wins: " + str(self.wins) + " losses: " + str(self.losses)


def champListFiller():
    URL = "http://ddragon.leagueoflegends.com/cdn/9.22.1/data/en_US/champion.json"
    response = requests.get(URL)
    return response.json()

def main():
    with open('matchdata.txt') as json_file:
        data = json.load(json_file)

    #print(data[0])
    j=0
    champsBanned = {}
    champsSelected = {}
    champsWin = {}
    champsLose = {}
    champs = champListFiller()
    for match in data:
        i=0
        for k in (0,1):
            for banned in data[j]['teams'][k]['bans']:
                champsBanned[data[j]['teams'][k]['bans'][i]['championId']] = champsBanned.get(data[j]['teams'][k]['bans'][i]['championId'], 0) + 1
        for participant in data[j]['participants']:
            champsSelected[data[j]['participants'][i]['championId']] = champsSelected.get(data[j]['participants'][i]['championId'], 0) + 1
            if data[j]['participants'][i]['stats']['win']:
                champsWin[data[j]['participants'][i]['championId']] = champsWin.get(data[j]['participants'][i]['championId'], 0) + 1
            else:
                champsLose[data[j]['participants'][i]['championId']] = champsLose.get(data[j]['participants'][i]['championId'], 0) + 1

            i+=1
        j+=1


    stuff = []
    for k,v in sorted(champsSelected.items(), key=lambda x: x[1]):
        for c in champs['data']:
            if champs['data'][c]['key'] == str(k):
                #print(champs['data'][c]['name'], v, champsBanned.get(k), champsWin.get(k), champsLose.get(k))
                stuff.append(champion(champs['data'][c]['name'], v, champsBanned.get(k), champsWin.get(k), champsLose.get(k)))
                #print(champs['data'][c]['name'], v, champsWin[k]/v, champsLose[k]/v)
                break

    for ch in stuff:
        print(ch)







main()
