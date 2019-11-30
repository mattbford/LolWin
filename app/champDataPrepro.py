## Takes Match data files and extracts champion statistic, outputs a json file
## Written by Rolin Buckoke 2019
## Altered by Matthew Belford 2019

import requests
import json
import datetime
import glob
import matplotlib.pyplot as pl
import pandas as pd
import operator
import time

class champion:

    def __init__(self, name, picks, bans, wins, losses, data, k):
        self.name = name
        self.picks = picks
        self.bans = bans
        self.wins = wins
        self.losses = losses
        self.vs = data["VS"].get(k)
        self.dmgObj = data["DmgObj"].get(k)
        self.ccDealt = data["ccDealt"].get(k)
        self.magicDmgDealt = data["magicDmgDealt"].get(k)
        self.phyDmgDealt = data["phyDmgDealt"].get(k)
        self.trueDmgDealt = data["trueDmgDealt"].get(k)
        self.kills = data["kills"].get(k)
        self.deaths = data["deaths"].get(k)
        self.assists = data["assists"].get(k)
        self.multiKill = data["multiKill"].get(k)
        self.killStreak = data["killStreak"].get(k)
        self.cs = data["CS"].get(k)
    def __str__(self):
        return "{\"Champion\": \"" +self.name + "\",\"Picks\": "+str(self.picks) + ",\"Bans:\":" + str(self.bans) + ",\"Wins:\":" + str(self.wins) + ",\"Losses:\":" + str(self.losses)
        + "\", \"visionScore\": \"" + str(self.vs) + "\", \"damageDealtToObjectives\": \"" + str(self.dmgObj) + "\", \"totalTimeCrowdControlDealt\": \"" + self.ccDealt
        + "\", \"magicDamageDealtToChampions\": \"" + self.magicDmgDealt + "\", \"physicalDamageDealtToChampions\": \"" + self.phyDmgDealt + "\", \"trueDamageDealt\": \""
        + self.trueDmgDealt + "\", \"kills\": \"" + self.kills + "\", \"deaths\": \"" + self.deaths + "\", \"assists\": \"" + self.assists + "\", \"largestMultikill\": \""
        + self.multiKill + "\", \"largestKillstreak\": \"" + self.killStreak + "\", \"cs\": \"" + self.cs +"\""
        + "}"
        #return self.name + " picks: " + str(self.picks) + " bans: " + str(self.bans) + " wins: " + str(self.wins) + " losses: " + str(self.losses)


def champListFiller():
    URL = "http://ddragon.leagueoflegends.com/cdn/9.22.1/data/en_US/champion.json"
    response = requests.get(URL)
    return response.json()

def main():
    #with open('datasets/matchData/matchData1574121600000.txt') as json_file:
    #    data = json.load(json_file)

    datasetsbyDate = {}
    for filename in glob.glob("datasets/matchData/matchData*.txt"):
        print("Running on Filename: " + filename)
        print("---------------------------------")
        date = filename[28:41] #just grabs the timestamp
        date = int(date)/1000
        date = time.strftime('%Y-%m-%d', time.localtime(date))
        with open(filename) as json_file:
            data = json.load(json_file)
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
                    champId = banned['championId']
                    champsBanned[champId] = champsBanned.get(champId, 0) + 1
            for participant in data[j]['participants']:
                champId = participant['championId']
                stats = participant['stats']
                champsSelected[champId] = champsSelected.get(champId, 0) + 1
                if stats['win']:
                    champsWin[champId] = champsWin.get(champId, 0) + 1
                else:
                    champsLose[champId] = champsLose.get(champId, 0) + 1
                i+=1
            j+=1

        champSpecs = {
            "VS": {},  # average vision scores for champ
            "DmgObj": {}, # average damage dealt to objectives
            "ccDealt": {}, # average time of cc dealt by champ
            "magicDmgDealt": {}, # average amount of magic damage dealt to champs
            "phyDmgDealt": {}, # average amount of physical damage dealt to champs
            "trueDmgDealt": {}, # average amount of true damage dealt
            "kills": {}, # average amount of kills per game
            "deaths": {}, # average amount of deaths per game
            "assists": {},  # average amount of assists per game
            "multiKill": {}, # average largest multikill per game
            "killStreak": {}, # average longest killing spree per game
            "CS":{} # average CS per game
        }


        j=0
        for match in data:
            i=0
            for participant in data[j]['participants']:
                champId = participant['championId']
                stats = participant['stats']
                champTotal = champsSelected[champId] # total games played

                champSpecs["VS"][champId] = champSpecs["VS"].get(champId, 0) + (stats['visionScore']/champTotal)
                champSpecs["DmgObj"][champId] = champSpecs["DmgObj"].get(champId, 0) + (stats['damageDealtToObjectives']/champTotal)
                champSpecs["ccDealt"][champId] = champSpecs["ccDealt"].get(champId, 0) + (stats['totalTimeCrowdControlDealt']/champTotal)
                champSpecs["magicDmgDealt"][champId] =  champSpecs["magicDmgDealt"].get(champId, 0) + (stats['magicDamageDealtToChampions']/champTotal)
                champSpecs["phyDmgDealt"][champId] = champSpecs["phyDmgDealt"].get(champId, 0) + (stats['physicalDamageDealtToChampions']/champTotal)
                champSpecs["trueDmgDealt"][champId] = champSpecs["trueDmgDealt"].get(champId, 0) + (stats['trueDamageDealt']/champTotal)
                champSpecs["kills"][champId] = champSpecs["kills"].get(champId, 0) + (stats['kills']/champTotal)
                champSpecs["deaths"][champId] = champSpecs["deaths"].get(champId, 0) + (stats['deaths']/champTotal)
                champSpecs["assists"][champId] = champSpecs["assists"].get(champId, 0) + (stats['assists']/champTotal)
                champSpecs["multiKill"][champId] = champSpecs["multiKill"].get(champId, 0) + (stats['largestMultiKill']/champTotal)
                champSpecs["killStreak"][champId] = champSpecs["killStreak"].get(champId, 0) + (stats['largestKillingSpree']/champTotal)
                champSpecs["CS"][champId] = champSpecs["CS"].get(champId, 0) + (stats['totalMinionsKilled']/champTotal)
            j+=1

        champdetails = []
        '''
        top5 = dict(sorted(champsSelected.items(), key=operator.itemgetter(1), reverse=True)[:5])
        x_13 = []
        for k in top5.keys():
            for c in champs['data']:
                if champs['data'][c]['key'] == str(k):
                    x_13.append(champs['data'][c]['name'])
        y_13 = top5.values()
        pl.xkcd()
        pl.bar(x_13, y_13, label = 'Champion Picks')
        pl.xlabel("Champion")
        pl.ylabel("Games Picked")
        pl.legend()
        pl.show()
        '''

        for k,v in sorted(champsSelected.items(), key=lambda x: x[1]):
            for c in champs['data']:
                if champs['data'][c]['key'] == str(k):
                    #print(champs['data'][c]['name'], v, champsBanned.get(k), champsWin.get(k), champsLose.get(k))
                    champdetails.append(champion(champs['data'][c]['name'], v, champsBanned.get(k), champsWin.get(k), champsLose.get(k), champSpecs, k))
                    #print(champs['data'][c]['name'], v, champsWin[k]/v, champsLose[k]/v)
                    break


        dailyArray = []
        for x in champdetails:
            dailyArray.append(json.dumps(x.__dict__))
        datasetsbyDate.update({date : dailyArray})

    for k in datasetsbyDate:
        with open("datasets/"+k+".json", 'w') as outfile:
            outfile.write("[")
            i = 0
            for c in datasetsbyDate[k]:
                if i+1 == len(datasetsbyDate[k]):
                    outfile.write(c)
                else:                    
                    temp = c + ","
                    outfile.write(temp)
                    
                i += 1
            outfile.write("]")
            #json.dump(datasetsbyDate[k], outfile)






main()
