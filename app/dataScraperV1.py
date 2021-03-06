## Uses the Riot Games API to scrape match data from the top 200 players
## Written by Matthew Belford 2019

import requests
import json
import time

from datetime import datetime
from datetime import timedelta
from dateutil import tz

apikey = "RGAPI-13feb37c-cec3-4ac6-8eba-480ea728339d" # dont forget to update every 24 hours
challengerReqUrl = "https://na1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5"
debug = True

# gets all 200 players in challenger from 
def getChallengerPlayers():
    URL =  challengerReqUrl + "?api_key=" + apikey #uses league v4
    response = requests.get(URL)
    return response.json()

# appends accountId to each player from challenger request as it is needed to find match history (approx. 5 minutes)
def getAccountIds(players):
    first = True
    for player in players:
        # infinite while loop allows redo of iteration if we run out of queries for that second
        URL = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}".format(player['summonerName'], apikey) #use summoner v4
        while True:            
            response = requests.get(URL)
            if debug:
                print(response.status_code)
            if response.status_code == 200:                
                summoner =  response.json()
                player['accountId'] = summoner['accountId']
                break
            elif response.status_code == 429:
                if debug:
                    print('HTTP ERROR: 429: too many requests: Waiting for 2 seconds')
                time.sleep(2)
                pass
            else:
                print('Unexpected HTTP ERROR: {}: exiting'.format(response.status_code))
                exit()

            
    return players

# gets a days worth of matchIds from each player in passed list using their accountId. Doesn't take duplicate matchIds. (approx. 5 minutes)
def getMatchIds(players, time_delt):
    matchIds = []

    #GET DATE of today - time_delt
    today = datetime.utcnow().date() - timedelta(time_delt)
    start = datetime(today.year, today.month, today.day, tzinfo=tz.tzutc())
    end = start + timedelta(1)
    end = int(datetime.timestamp(end) * 1000)
    start = int(datetime.timestamp(start) * 1000)

    for player in players:
        # ranked solo/duo queueId = 420, max 20 game index
        URL = "https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?queue=420&endTime={}&beginTime={}&endIndex=20&api_key={}".format(player['accountId'], end, start, apikey)
        while True:
            response = requests.get(URL)
            if debug:
                print(response.status_code)
            if response.status_code == 200:                
                matchList = response.json()
                for match in matchList['matches']:
                    if match['gameId'] not in matchIds:
                        matchIds.append(match['gameId'])
                break                    
            elif response.status_code == 429:
                if debug:
                    print('HTTP ERROR: 429: too many requests: Waiting for 2 seconds')
                time.sleep(2)
                pass
            elif response.status_code == 404:
                if debug:
                    print('HTTP ERROR: 404: no matches today')
                break
            elif response.status_code == 503:
                if debug:
                    print('HTTP ERROR: 503: service unavailable waiting')
                time.sleep(2)
                pass
            else:
                print('Unexpected HTTP ERROR: {}: exiting'.format(response.status_code))
                exit()
    return matchIds, start

# gets match data from list of matchIds. (Max runtime: 80 mintues)
def getMatchData(matches):
    matchData = []
    for match in matches:
        URL = "https://na1.api.riotgames.com/lol/match/v4/matches/{}?api_key={}".format(match, apikey)
        while True:
            response = requests.get(URL)
            if debug:
                print(response.status_code)
            if response.status_code == 200:
                matchData.append(response.json())
                break
            elif response.status_code == 429:
                if debug:
                    print('HTTP ERROR: 429: too many requests: Waiting for 2 seconds')
                time.sleep(2)
                pass
            else:
                print('Unexpected HTTP ERROR: {} skipping'.format(response.status_code))
                break
    return matchData

def main():

    # change array range to go time_delt days back (used to get multiple days worth of data)
    for time_delt in [0]:
        # get challenger players and append their accountIds to their data
        print("get challenger players")
        challengerResponse = getChallengerPlayers()
        players = challengerResponse['entries']

        print("get account ids")
        players = getAccountIds(players)
        #with open('datasets/Old/challengerPlayers.txt', 'w+') as playersfile:
        #    json.dump(players, playersfile)

        #read the challenger players json file and get matches
        #players = []
        #with open('datasets/Old/challengerPlayers.txt') as json_file:
        #    players = json.load(json_file)

        print("get match ids")
        matches, date = getMatchIds(players, time_delt)
        
        #filename = "datasets/Old/matchIds{}.txt".format(date)
        #with open(filename, "w+") as matchIdsFile:
        #    for match in matches:
        #        matchIdsFile.write("{}\n".format(match))

        #read the matchIds file and get match data

        # dont need this if matchIds is run first
        #today = datetime.utcnow().date()
        #date = datetime(today.year, today.month, today.day, tzinfo=tz.tzutc())
        #date = int(datetime.timestamp(date) * 1000)
        #matches = []
        #with open("datasets/Old/matchIds1574121600000.txt") as match_file:
        #    for line in match_file:
        #        matches.append(line.strip('\n'))

        print("Number of matches being scooped: " + str(len(matches)))
        matchData = getMatchData(matches)
        filename = "datasets/matchData/matchData{}.txt".format(date)
        
        with open(filename, "w+") as matchDataFile:
            json.dump(matchData, matchDataFile)
    

main()