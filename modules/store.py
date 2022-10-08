from requests import get
from modules.api import get_store_weapons
import json

def GetStore(needs):
    puuid = needs[2]
    entitlement = needs[1]
    token = needs[0]
    region = needs[3]
    headers = {
        'X-Riot-Entitlements-JWT': entitlement,
        'Authorization': f'Bearer {token}'
    }
    resp = get(f'https://pd.{region}.a.pvp.net/store/v2/storefront/{puuid}', headers=headers).text
    r = json.loads(resp)
    skinsuuid = r['SkinsPanelLayout']['SingleItemOffers']
    return get_store_weapons(skinsuuid)

def GetSkinsUuids(needs): ## needed for retriving the prices of the skins
    puuid = needs[2]
    entitlement = needs[1]
    token = needs[0]
    region = needs[3]
    headers = {
        'X-Riot-Entitlements-JWT': entitlement,
        'Authorization': f'Bearer {token}'
    }
    resp = get(f'https://pd.{region}.a.pvp.net/store/v2/storefront/{puuid}', headers=headers).text
    r = json.loads(resp)
    skinsuuid = r['SkinsPanelLayout']['SingleItemOffers']
    return skinsuuid

def price_retriver(skinuuid, offers_data):
    for row in offers_data["Offers"]:
        if row["OfferID"] == skinuuid:
            for cost in row["Cost"]:
                return row["Cost"][cost]

def GetStorePrices(needs):
    puuid = needs[2]
    entitlement = needs[1]
    token = needs[0]
    region = needs[3]

    skins_price = []
    headers2 = {'Authorization': f'Bearer {token}', 'X-Riot-Entitlements-JWT': entitlement, 'Content-Type': 'text/plain'}
    of_data = get(f"https://pd.{region}.a.pvp.net/store/v1/offers/", headers=headers2)
    offers_data = of_data.json()
    weapon_fetch = get(f'https://valorant-api.com/v1/weapons/skinlevels')
    weapon_fetch = weapon_fetch.json()
    daily_items = GetSkinsUuids(needs)
    for skin in daily_items:
        for row in weapon_fetch["data"]:
            if skin == row["uuid"]:
                skin_price = price_retriver(skin, offers_data)
                skins_price.append(skin_price)
    return skins_price
