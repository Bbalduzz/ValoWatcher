from typing import List
from requests import get
import json

# API USED = https://valorant-api.com

def GetCurrentCollection(loadout):
    names = [] 
    icons = []
    for gun in loadout:
        skin = gun['ChromaID']
        skinchroma = get(f'https://valorant-api.com/v1/weapons/skinchromas/{skin}').json()
        name, icon = skinchroma['data']['displayName'].replace('\r','').replace('\n', ' - '), skinchroma['data']['displayIcon']
        names.append(name)
        icons.append(icon)
    
    collection = dict(zip(names, icons))
    return collection


## THIS SLOW THINGS DOWN  !! todo: threading to make it faster
def get_things(possession: dict, type: str) -> List:
    possessions = []
    for n in range(len(possession['Entitlements'])):
        elem = possession['Entitlements'][n]['ItemID']
        elem_obj = get(f'https://valorant-api.com/v1/{type}/{elem}').json()
        try:
            elem_name = elem_obj['data']['displayName']
            possessions.append(elem_name)
        except KeyError:
            pass
        n += 1
    return possessions

def RedablePlayerContent(agents, contracts, sprays, buddies, playercards, playertitles):
    
    your_agents = get_things(agents, 'agents')

    contract = contracts['Entitlements'][0]['ItemID']
    contract_obj = get(f'https://valorant-api.com/v1/contracts/{contract}').json()
    contract_name = contract_obj['data']['displayName']

    your_spray = get_things(sprays, 'sprays')
    your_buddies = get_things(buddies, 'buddies')
    your_cards = get_things(playercards, 'playercards')
    your_titles = get_things(playertitles, 'playertitles')

    return [your_agents, contract_name, your_spray, your_buddies, your_cards, your_titles]

def get_store_weapons(offers):
    weapons_names = []
    for offer_id in offers:
        weapon = get(f'https://valorant-api.com/v1/weapons/skinlevels/{offer_id}').json()['data']['displayName']
        weapons_names.append(weapon)
    return weapons_names

def get_nightmarket_skins(offers, prices):
    skins = []
    for nmskinid in offers:
        with get(f'https://valorant-api.com/v1/weapons/skinlevels/{nmskinid}') as r:
            nmdata = r.json()
        skins.append(nmdata['data']['displayName'])

    return dict(zip(skins, prices))
        

    