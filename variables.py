from modules.mmr import GetMMR
from modules.auth import Auth
from modules.loadout import GetLoadout
from modules.playercontent import GetPlayerContent
from modules.store import GetStore, GetStorePrices
from modules.player import get_player_id, get_player_balances, get_player_progress
from modules.nightmarket import GetNightMarket
from modules.matches import GetMatches

import os
import configparser
config = configparser.ConfigParser()		
parentdir = os.path.dirname(__file__)
os.path.abspath(os.path.join(parentdir, os.pardir))
config.read("/".join([parentdir,"config.ini"]))
from prettytable import PrettyTable
x = PrettyTable()

def choose_account():
    global username, password, region
    accounts = config.sections()
    usernames = [config[a]['riot_username'] for a in accounts]
    ids = [i for i in range(len(usernames))]

    x.add_column('ID', ids)
    x.add_column('Username', usernames)
    print(x)

    choice = int(input('What account do u want to watch? [ID]: '))
    acc = config[f'ACCOUNT{choice+1}']
    username = acc['riot_username']
    password = acc['password']
    region = acc['region']

    return f'{username}:{password}:{region}'


## account & infos ##
acc =  choose_account()
needs = Auth(acc) # get the token, entitlement and puuid

## data ##
mmr = GetMMR(acc,needs)
# player_content = GetPlayerContent(needs) --> this slow things down
loadout = GetLoadout(acc, needs)
store = GetStore(needs)
store_prices = GetStorePrices(needs)
full_store = dict(zip(store, store_prices)) # just to associate each skin with its own price
playerID = get_player_id(needs)
player_balances= get_player_balances(needs)
player_valorantpoints, player_radianite = player_balances[0], player_balances[1]
player_progression = get_player_progress(needs)
player_level, player_xp = player_progression[0], player_progression[1]
nightmarket_store = GetNightMarket(needs)

matches_results, competitive_matches_results = GetMatches(needs)
winorlost = matches_results[0]
agets_played = matches_results[1]
kills_deaths_assists = matches_results[2]

##### DEBUG
# print(playerID)
# print(player_valorantpoints, player_radianite)
# print(mmr)

# print(loadout)

# for item in store:
#     print(item, '-->', full_store[item])

# print(player_level, player_xp)
# print(nightmarket_store)

# print(winorlost)