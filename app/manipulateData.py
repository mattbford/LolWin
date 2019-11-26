import requests
import json
import datetime
import glob
import matplotlib.pyplot as pl
import pandas as pd
import operator
import time

class champion:

    def __init__(self, name, picks, bans, wins, losses):
        self.name = name
        self.picks = picks
        self.bans = bans
        self.wins = wins
        self.losses = losses
    def __str__(self):
        return "{Champion: \"" +self.name + "\",\"Picks\": "+str(self.picks) + ",\"Bans:\":" + str(self.bans) + ",\"Wins:\":" + str(self.wins) + ",\"Losses:\":" + str(self.losses) + "}"

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
                    champsBanned[data[j]['teams'][k]['bans'][i]['championId']] = champsBanned.get(data[j]['teams'][k]['bans'][i]['championId'], 0) + 1
            for participant in data[j]['participants']:
                champsSelected[data[j]['participants'][i]['championId']] = champsSelected.get(data[j]['participants'][i]['championId'], 0) + 1
                if data[j]['participants'][i]['stats']['win']:
                    champsWin[data[j]['participants'][i]['championId']] = champsWin.get(data[j]['participants'][i]['championId'], 0) + 1
                else:
                    champsLose[data[j]['participants'][i]['championId']] = champsLose.get(data[j]['participants'][i]['championId'], 0) + 1

                i+=1
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
                    champdetails.append(champion(champs['data'][c]['name'], v, champsBanned.get(k), champsWin.get(k), champsLose.get(k)))
                    #print(champs['data'][c]['name'], v, champsWin[k]/v, champsLose[k]/v)
                    break


        dailyArray = []
        for x in champdetails:
            dailyArray.append(json.dumps(x.__dict__))
        datasetsbyDate.update({date : dailyArray})

    for k in datasetsbyDate:
        with open("datasets/"+k+".json", 'w') as outfile:
            outfile.write("[")
            for c in datasetsbyDate[k]:
                outfile.write(c)
            outfile.write("]")
            #json.dump(datasetsbyDate[k], outfile)






main()
