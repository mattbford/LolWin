import requests
import json
import datetime
import glob
import matplotlib.pyplot as pl
import pandas as pd
import operator
import time


class matchData():
    winner = None
    t1firstdrag =None
    t1firstinhib=None
    t1firstherald=None
    t1firstbaron=None
    t1firsttower=None
    t1barons=None
    t1dragons=None
    t1vision=None
    t1towers=None
    t1cc=None
    t1kills=None
    t1assists=None
    t1deaths=None
    t1cs=None
    t1gold=None
    t2firstdrag=None
    t2firstinhib=None
    t2firstherald=None
    t2firstbaron=None
    t2firsttower=None
    t2barons=None
    t2dragons=None
    t2vision=None
    t2towers=None
    t2cc=None
    t2kills=None
    t2assists=None
    t2deaths=None
    t2cs=None
    t2gold =None

    def __init__(self):
        pass

    def __str__(self):
        return "a"

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

def main():

    for filename in glob.glob("datasets/matchData/matchData*.txt"):
        #print("Running on Filename: " + filename)
        #print("---------------------------------")
        date = filename[28:41] #just grabs the timestamp
        date = int(date)/1000
        date = time.strftime('%Y-%m-%d', time.localtime(date))
        with open(filename) as json_file:
            data = json.load(json_file)

        matches = []
        i=0
        for match in data:
            x = matchData()
            if (data[i]['teams'][0]['win'] == 'Win'):
                x.winner = 1
            else:
                x.winner=2
            x.t1firstdrag = data[i]['teams'][0]['firstDragon']
            x.t1firstinhib = data[i]['teams'][0]['firstInhibitor']
            x.t1firstherald = data[i]['teams'][0]['firstRiftHerald']
            x.t1firstbaron = data[i]['teams'][0]['firstBaron']
            x.t1firsttower = data[i]['teams'][0]['firstTower']
            x.t1firsttower = data[i]['teams'][0]['win']
            x.t1barons = data[i]['teams'][0]['baronKills']
            x.t1dragons = data[i]['teams'][0]['dragonKills']
            x.t1towers = data[i]['teams'][0]['towerKills']
            #team2stuff
            x.t2firstdrag = data[i]['teams'][1]['firstDragon']
            x.t2firstinhib = data[i]['teams'][1]['firstInhibitor']
            x.t2firstherald = data[i]['teams'][1]['firstRiftHerald']
            x.t2firstbaron = data[i]['teams'][1]['firstBaron']
            x.t2firsttower = data[i]['teams'][1]['firstTower']
            x.t2barons = data[i]['teams'][1]['baronKills']
            x.t2dragons = data[i]['teams'][1]['dragonKills']
            x.t2towers = data[i]['teams'][1]['towerKills']
            totalVision=0
            totalCC=0
            totalKills=0
            totalDeaths=0
            totalCS=0
            totalGold=0
            totalAssists=0
            for j in range(0,4):
                totalVision+=data[i]['participants'][j]['stats']['visionScore']
                totalCC+=data[i]['participants'][j]['stats']['timeCCingOthers']
                totalKills+=data[i]['participants'][j]['stats']['kills']
                totalKills+=data[i]['participants'][j]['stats']['assists']
                totalDeaths+=data[i]['participants'][j]['stats']['deaths']
                totalCS+=data[i]['participants'][j]['stats']['totalMinionsKilled']
                totalGold+=data[i]['participants'][j]['stats']['goldEarned']
            x.t1vision = totalVision
            x.t1cc = totalCC
            x.t1kills = totalKills
            x.t1assists = totalAssists
            x.t1deaths = totalDeaths
            x.t1cs = totalCS
            x.t1gold = totalGold
            totalVision=0
            totalCC=0
            totalKills=0
            totalDeaths=0
            totalCS=0
            totalGold=0
            totalAssists=0
            for j in range(5,9):
                totalVision+=data[i]['participants'][j]['stats']['visionScore']
                totalCC+=data[i]['participants'][j]['stats']['timeCCingOthers']
                totalKills+=data[i]['participants'][j]['stats']['kills']
                totalKills+=data[i]['participants'][j]['stats']['assists']
                totalDeaths+=data[i]['participants'][j]['stats']['deaths']
                totalCS+=data[i]['participants'][j]['stats']['totalMinionsKilled']
                totalGold+=data[i]['participants'][j]['stats']['goldEarned']
            x.t2vision = totalVision
            x.t2cc = totalCC
            x.t2kills = totalKills
            x.t2assists = totalAssists
            x.t2deaths = totalDeaths
            x.t2cs = totalCS
            x.t2gold = totalGold
            matches.append(x)

        for match in  matches:
            print(x.toJSON()+",")


main()
