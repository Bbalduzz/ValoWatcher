from requests import get
from modules.api import get_nightmarket_skins

def GetNightMarket(needs):
    token = needs[0]
    puuid = needs[2]
    entitlement = needs[1]
    region = needs[3]

    headers2 = {'Authorization': f'Bearer {token}', 'X-Riot-Entitlements-JWT': entitlement, 'Content-Type': 'text/plain'}
    with get(f'https://pd.{region}.a.pvp.net/store/v2/storefront/{puuid}', headers=headers2, json=[puuid]) as r:
        data = r.json()
    nm_price = []
    nm_offers = []
    nm_images = []
    nm_skins_id = []
    try:
        for i in data['BonusStore']['BonusStoreOffers']:
            [nm_price.append(k) for k in i['DiscountCosts'].values()] # night market prices
        for i in data['BonusStore']['BonusStoreOffers']:
            [nm_skins_id.append(k['ItemID']) for k in i['Offer']['Rewards']] # night market offers
    except KeyError:
        for i in range(6):
            nm_skins_id.append('NONE')
        for i in range(6):
            nm_price.append('NONE')

    return get_nightmarket_skins(nm_skins_id, nm_price)