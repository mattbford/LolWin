import requests
import json
import datetime
#Global var

#https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/zynz?api_key=RGAPI-c948d1cc-eacd-4e6b-bd3f-2144baf8e6e1
#name = "zynz"
key=""
#summoner_id = "https://na.api.riotgames.com/lol/summoner/v4/"
def request(name):
    print("Request Done")
    URL = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}".format(name,key)
    response = requests.get(URL)
    return response.json()

def requestMatches(accountId):
    yesterday = datetime.date.today() - datetime.timedelta(7)
    yesterday = yesterday.strftime("%s")
    yesterday = yesterday + "000"
    print("Using id: " + accountId)
    print(yesterday)
    URL = "https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?queue=420&beginTime={}&api_key={}".format(accountId,yesterday,key)
    response = requests.get(URL)
    return response.json()

def champListFiller():
    URL = "http://ddragon.leagueoflegends.com/cdn/9.22.1/data/en_US/champion.json"
    response = requests.get(URL)
    return response.json()

def getChampions():
    URL = "https://na1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key={}".format(key)
    response = requests.get(URL)
    return response.json()



def main():
    player_match_df_list = {}
    name = input('Name: ')
    account = request(name)
    print(account)
    print(account['accountId'])
    matches = requestMatches(account['accountId'])
    champs = champListFiller()
    for match in matches['matches']:
        champ = match['champion']
        for c in champs['data']:
            if champs['data'][c]['key'] == str(champ):
                print(champs['data'][c]['name'])
                break
    #print(champs['data']['Aatrox']['key'])
    #c = c for c in champs if champs['data']['key'==champ]
    #print(c)

#This yields a list of last 10 games played (This varies between player and Season)
main()
