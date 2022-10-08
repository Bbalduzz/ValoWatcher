from modules.auth import Auth
from requests import get
import json

def GetMMR(account, needs):
    token = needs[0]
    entitlement = needs[1]
    puuid = needs[2]
    region = needs[3]
    headers = {
        'X-Riot-Entitlements-JWT': entitlement,
        'Authorization': f'Bearer {token}',
        'X-Riot-ClientVersion': 'release-05.06-shipping-6-765767',
        'X-Riot-ClientPlatform':'ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9'
    }

    mmrreq = get(f'https://pd.{region}.a.pvp.net/mmr/v1/players/{puuid}', headers=headers).json()
    # with open('./loadout.json', 'r+') as f: f.write(json.dumps(mmrreq))
    return mmrreq['LatestCompetitiveUpdate']['RankedRatingAfterUpdate']

