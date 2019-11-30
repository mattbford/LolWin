import requests
import datetime
import glob
import matplotlib.pyplot as pl
import pandas as pd
import operator
import time
import csv


class matchData():
    winner = None
    firstdrag =None
    firstinhib=None
    firstherald=None
    firstbaron=None
    firsttower=None
    barons=None
    dragons=None
    vision=None
    towers=None
    cc=None
    kills=None
    assists=None
    deaths=None
    cs=None
    gold=None


    def __init__(self):
        pass

    def __str__(self):
        return "a"

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

def main():
    with open("week_data.csv", mode="w+", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['Winner', 'First Dragon', 'First Inhibitor', 'First Rift Herald', 'First Baron Nashor', 'First Tower',
        'Barons', 'Dragons', 'Vision Score', 'Towers Taken', 'Time of CC Dealt', 'Kills', 'Assists', 'Deaths', 'Creep Score', 'Gold'])

        for filename in glob.glob("datasets/matchData/matchData*.txt"):
            #print("Running on Filename: " + filename)
            #print("---------------------------------")
            date = filename[28:41] #just grabs the timestamp
            date = int(date)/1000
            date = time.strftime('%Y-%m-%d', time.localtime(date))
            with open(filename) as json_file:
                data = json.load(json_file)

            #matches = []
            i=0
            for match in data:
                # since matches have the data for two teams make each a separate object
                x1 = matchData()
                x2 = matchData()

                if (data[i]['teams'][0]['win'] == 'Win'):
                    x1.winner = True
                    x2.winner = False
                else:
                    x1.winner = False
                    x2.winner = True

                # first get all data for team one
                x1.firstdrag = data[i]['teams'][0]['firstDragon']
                x1.firstinhib = data[i]['teams'][0]['firstInhibitor']
                x1.firstherald = data[i]['teams'][0]['firstRiftHerald']
                x1.firstbaron = data[i]['teams'][0]['firstBaron']
                x1.firsttower = data[i]['teams'][0]['firstTower']
                x1.barons = data[i]['teams'][0]['baronKills']
                x1.dragons = data[i]['teams'][0]['dragonKills']
                x1.towers = data[i]['teams'][0]['towerKills']
                totalVision=0
                totalCC=0
                totalKills=0
                totalDeaths=0
                totalCS=0
                totalGold=0
                totalAssists=0
                for j in range(0,9):
                    totalVision+=data[i]['participants'][j]['stats']['visionScore']
                    totalCC+=data[i]['participants'][j]['stats']['timeCCingOthers']
                    totalKills+=data[i]['participants'][j]['stats']['kills']
                    totalAssists+=data[i]['participants'][j]['stats']['assists']
                    totalDeaths+=data[i]['participants'][j]['stats']['deaths']
                    totalCS+=data[i]['participants'][j]['stats']['totalMinionsKilled']
                    totalGold+=data[i]['participants'][j]['stats']['goldEarned']
                x1.vision = totalVision
                x1.cc = totalCC
                x1.kills = totalKills
                x1.assists = totalAssists
                x1.deaths = totalDeaths
                x1.cs = totalCS
                x1.gold = totalGold

                # write data for team one to csv
                csv_writer.writerow([x1.winner, x1.firstdrag, x1.firstinhib, x1.firstherald, x1.firstbaron, x1.firsttower, x1.barons,
                x1.dragons, x1.vision, x1.towers, x1.cc, x1.kills, x1.assists, x1.deaths, x1.cs, x1.gold])

                # now get all data for team two
                x2.firstdrag = data[i]['teams'][0]['firstDragon']
                x2.firstinhib = data[i]['teams'][0]['firstInhibitor']
                x2.firstherald = data[i]['teams'][0]['firstRiftHerald']
                x2.firstbaron = data[i]['teams'][0]['firstBaron']
                x2.firsttower = data[i]['teams'][0]['firstTower']
                x2.barons = data[i]['teams'][0]['baronKills']
                x2.dragons = data[i]['teams'][0]['dragonKills']
                x2.towers = data[i]['teams'][0]['towerKills']

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
                    totalAssists+=data[i]['participants'][j]['stats']['assists']
                    totalDeaths+=data[i]['participants'][j]['stats']['deaths']
                    totalCS+=data[i]['participants'][j]['stats']['totalMinionsKilled']
                    totalGold+=data[i]['participants'][j]['stats']['goldEarned']
                x2.vision = totalVision
                x2.cc = totalCC
                x2.kills = totalKills
                x2.assists = totalAssists
                x2.deaths = totalDeaths
                x2.cs = totalCS
                x2.gold = totalGold

                # write team two data
                csv_writer.writerow([x2.winner, x2.firstdrag, x2.firstinhib, x2.firstherald, x2.firstbaron, x2.firsttower, x2.barons,
                x2.dragons, x2.vision, x2.towers, x2.cc, x2.kills, x2.assists, x2.deaths, x2.cs, x2.gold])
                i+=1


main()
