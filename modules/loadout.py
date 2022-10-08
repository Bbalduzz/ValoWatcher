import requests
from modules.api import GetCurrentCollection

def GetLoadout(account, needs):
    token = needs[0]
    entitlement = needs[1]
    puuid = needs[2]
    region = needs[3]

    headers = {
        'X-Riot-Entitlements-JWT': entitlement,
        'Authorization': f'Bearer {token}'
    }

    r = requests.get(f'https://pd.{region}.a.pvp.net/personalization/v2/players/{puuid}/playerloadout', headers=headers)
    data = r.json()
    collection = GetCurrentCollection(data['Guns'])
    return collection