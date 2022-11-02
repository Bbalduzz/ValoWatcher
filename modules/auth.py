from requests import session as sesh
from requests.adapters import HTTPAdapter
from ssl import PROTOCOL_TLSv1_2
from urllib3 import PoolManager
from collections import OrderedDict
from re import compile
from rich.console import Console
c = Console()

class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize, block=block,
                                       ssl_version=PROTOCOL_TLSv1_2)

def Auth(line):
    user_agent = 'RiotClient/60.0.3.4751956.4749685 rso-auth (Windows;10;;Professional, x64)'
    username = line.split(":")[0].replace('\n', '')
    password = line.split(":")[1].replace('\n', '')
    region = line.split(":")[2].replace('\n', '')
    headers = OrderedDict({
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "application/json, text/plain, */*",
        'User-Agent': user_agent
    })
    session = sesh()
    session.headers = headers #type:ignore
    session.mount('https://', TLSAdapter())
    data = {
        "client_id": "play-valorant-web-prod",
        "nonce": "1",
        "redirect_uri": "https://playvalorant.com/opt_in",
        "response_type": "token id_token",
        'scope': 'account openid',
    }
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': user_agent
    }
    r = session.post(f'https://auth.riotgames.com/api/v1/authorization', json=data, headers=headers)
    data = {
        'type': 'auth',
        'username': username,
        'password': password
    }
    r2 = session.put('https://auth.riotgames.com/api/v1/authorization', json=data, headers=headers)
    data = r2.json()
    if "access_token" in r2.text:
        pattern = compile(
            'access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
        data = pattern.findall(data['response']['parameters']['uri'])[0]
        token = data[0]

    elif "auth_failure" in r2.text:
        print("banned")
    else:
        ver_code = c.input('[b][green]2FA Auth Enabled[/green][/b]. Enter the verification code: \n')
        authdata = {
            'type': 'multifactor',
            'code': ver_code,
        }
        r = session.put('https://auth.riotgames.com/api/v1/authorization', json=authdata, headers=headers)
        data = r.json()
        if "access_token" in r.text:
            pattern = compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
            data = pattern.findall(data['response']['parameters']['uri'])[0]
            token = data[0]
        elif "auth_failure" in r.text:
            print("Banned")
        else:
            print('Failed')
    headers = {
        'User-Agent': user_agent,
        'Authorization': f'Bearer {token}',
    }
    r = session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={})
    entitlement = r.json()['entitlements_token']
    r = session.post('https://auth.riotgames.com/userinfo', headers=headers, json={})
    data = r.json()
    puuid = data['sub']

    return [token, entitlement, puuid, region]
