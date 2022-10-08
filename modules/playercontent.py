from requests import get
from modules.api import RedablePlayerContent
import json

def GetPlayerContent(needs):
    puuid = needs[2]
    entitlement = needs[1]
    token = needs[0]
    region = needs[3]
    headers = {
        'X-Riot-Entitlements-JWT': entitlement,
        'Authorization': f'Bearer {token}'
    }
    key_items_id = ['01bb38e1-da47-4e6a-9b3d-945fe4655707', 'f85cb6f7-33e5-4dc8-b609-ec7212301948', 'd5f120f8-ff8c-4aac-92ea-f2b5acbe9475', 'dd3bf334-87f3-40bd-b043-682a57a8dc3a', '3f296c07-64c3-494c-923b-fe692a4fa1bd', 'e7c63390-eda7-46e0-bb7a-a6abdacd2433', '3ad1b2b2-acdb-4524-852f-954a76ddae0a','de7caa6b-adf7-4588-bbd1-143831e786c6']
    value_items_id = ['Agents', 'Contracts', 'Sprays', 'Gun Buddies', 'Cards', 'Skins', 'Skin Variants', 'Titles']
    items_dict_id = dict(zip(value_items_id, key_items_id))
    owned_agents = get(f'https://pd.{region}.a.pvp.net/store/v1/entitlements/{puuid}/{items_dict_id["Agents"]}', headers=headers).text
    active_contract = get(f'https://pd.{region}.a.pvp.net/store/v1/entitlements/{puuid}/{items_dict_id["Contracts"]}', headers=headers).text
    owned_sprays = get(f'https://pd.{region}.a.pvp.net/store/v1/entitlements/{puuid}/{items_dict_id["Sprays"]}', headers=headers).text
    owned_buddies = get(f'https://pd.{region}.a.pvp.net/store/v1/entitlements/{puuid}/{items_dict_id["Gun Buddies"]}', headers=headers).text
    owned_cards = get(f'https://pd.{region}.a.pvp.net/store/v1/entitlements/{puuid}/{items_dict_id["Cards"]}', headers=headers).text
    # owned_skins = get(f'https://pd.{region}.a.pvp.net/store/v1/entitlements/{puuid}/{items_dict_id["Skins"]}', headers=headers).text
    # owned_skinsvar = get(f'https://pd.{region}.a.pvp.net/store/v1/entitlements/{puuid}/{items_dict_id["Skin Variants"]}', headers=headers).text
    owned_titles = get(f'https://pd.{region}.a.pvp.net/store/v1/entitlements/{puuid}/{items_dict_id["Titles"]}', headers=headers).text

    favourites = get(f'https://pd.{region}.a.pvp.net/favorites/v1/players/{puuid}/favorites', headers=headers).text # just to have it here, im not using it

    return RedablePlayerContent(json.loads(owned_agents), json.loads(active_contract), json.loads(owned_sprays), json.loads(owned_buddies), json.loads(owned_cards), json.loads(owned_titles))
    