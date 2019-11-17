"""
setup this file to be run once a day

Plan:

Get all challenger summoner IDs

Scrape last 20 games from each summoner
    get the data: Champion and win/loss

output to JSON File every 100 games.


"""

import requests
import json
import time

apikey = "RGAPI-56e1ebea-d11a-4b70-9caf-f8f5052de9ab" # dont forget to update every 24 hours
challengerReqUrl = "https://na1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5"
debug = True

# gets all 200 players in challenger from 
def getChallengerPlayers():
    URL =  challengerReqUrl + "?api_key=" + apikey
    response = requests.get(URL)
    return response.json()

# appends accountId to each player from challenger request as it is needed to find match history (approx. 5 minutes)
def getAccountIds(players):
    first = True
    for player in players:
        # infinite while loop allows redo of iteration if we run out of queries for that second
        URL = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}".format(player['summonerName'], apikey)
        while True:            
            response = requests.get(URL)
            print(response.status_code)
            if response.status_code == 200:                
                summoner =  response.json()
                player['accountId'] = summoner['accountId']
                break
            elif response.status_code == 429:
                print('HTTP ERROR: 429: too many requests: Waiting for 2 seconds')
                time.sleep(2)
                pass
            else:
                print('Unexpected HTTP ERROR: {}: exiting'.format(response.status_code))
                exit()

            
    return players

# gets last 20 matchIds from each player in passed list using their accountId. Doesn't take duplicate matchIds. (approx. 40 minutes)
def getMatchIds(players):
    matchIds = []
    for player in players:
        URL = "https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?endIndex=20&api_key={}".format(player['accountId'], apikey)
        while True:
            response = requests.get(URL)
            print(response.status_code)
            if response.status_code == 200:                
                matchList = response.json()
                for match in matchList['matches']:
                    if match['gameId'] not in matchIds:
                        matchIds.append(match['gameId'])
                break
                    
            elif response.status_code == 429:
                print('HTTP ERROR: 429: too many requests: Waiting for 2 seconds')
                time.sleep(2)
                pass
            else:
                print('Unexpected HTTP ERROR: {}: exiting'.format(response.status_code))
                exit()
    return matchIds

# gets match data from list of matchIds. (Max runtime: 80 mintues Approx. 40 minutes)
#def getMatchData(players):



def main():

    # get challenger players and append their accountIds to their data
    #challengerResponse = getChallengerPlayers()
    #players = challengerResponse['entries']
    #players = getAccountIds(players)
    #with open('datasets/challengerPlayers.txt', 'w+') as playersfile:
    #    json.dump(players, playersfile)

    #read the challenger players json file and get matches
    players = []
    with open('datasets/challengerPlayers.txt') as json_file:
        players = json.load(json_file)

    matches = getMatchIds(players)

    with open("datasets/matchIds.txt", "w+") as matchIdsFile:
        for match in matches:
            matchIdsFile.write("{}\n".format(match))

main()