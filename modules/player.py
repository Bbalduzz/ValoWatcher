from requests import post, get

def get_player_id(needs):
    entitlement = needs[1]
    token = needs[0]
    user_agent = 'RiotClient/60.0.3.4751956.4749685 rso-auth (Windows;10;;Professional, x64)'
    headers = {
        'User-Agent': user_agent,
        'X-Riot-Entitlements-JWT': entitlement,
        'Authorization': f'Bearer {token}'
    }
    r = post('https://auth.riotgames.com/userinfo', headers=headers, json={})
    data = r.json()
    name = data['acct']['game_name']+'#'+data['acct']['tag_line']
    return name

def get_player_balances(needs):
    entitlement = needs[1]
    token = needs[0]
    region = needs[3]
    headers = {
        'User-Agent': 'RiotClient/58.0.0.4640299.4552318 rso-auth (Windows;10;;Professional, x64)',
        'X-Riot-Entitlements-JWT': entitlement,
        'Authorization': f'Bearer {token}'
    }
    r = post('https://auth.riotgames.com/userinfo', headers=headers, json={})
    sub = r.text.split('sub":"')[1].split('"')[0]
    headers2 = {'Authorization': f'Bearer {token}', 'X-Riot-Entitlements-JWT': entitlement, 'Content-Type': 'text/plain'}
    GetPoints = get(f"https://pd.{region}.a.pvp.net/store/v1/wallet/{sub}",headers=headers2)
    ValorantPoints = GetPoints.json()["Balances"]["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"]
    Radianite = GetPoints.json()["Balances"]["e59aa87c-4cbf-517a-5983-6e81511be9b7"]
    return [ValorantPoints, Radianite]

def get_player_progress(needs):
    token = needs[0]
    entitlement = needs[1]
    puuid = needs[2]
    region = needs[3]
    headers = {
        'X-Riot-Entitlements-JWT': entitlement,
        'Authorization': f'Bearer {token}'
    }
    r = get(f'https://pd.{region}.a.pvp.net/account-xp/v1/players/{puuid}', headers=headers).json()
    level, xp = r['Progress']['Level'], r['Progress']['XP']
    return [level, xp]
