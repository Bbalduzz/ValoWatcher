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

class RiotClient:
    def __init__(self, line):
        self.username = line.split(":")[0].replace('\n', '')
        self.password = line.split(":")[1].replace('\n', '')

    def get_needs(self, username, password):
        user_agent = 'RiotClient/60.0.3.4751956.4749685 rso-auth (Windows;10;;Professional, x64)'
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
            'User-Agent': user_agent,
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
            id_token = data[1]

        elif "auth_failure" in r2.text:
            pass
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
                id_token = data[1]
            elif "auth_failure" in r.text:
                pass
            else:
               pass
        headers = {
            'User-Agent': user_agent,
            'Authorization': f'Bearer {token}',
        }
        r = session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={})
        entitlement = r.json()['entitlements_token']
        r = session.post('https://auth.riotgames.com/userinfo', headers=headers, json={})
        data = r.json()
        puuid = data['sub']

        reg_json = {'id_token': id_token}
        r = session.put('https://riot-geo.pas.si.riotgames.com/pas/v1/product/valorant',json=reg_json, headers=headers)
        region = r.json()['affinities']['live']

        return token, entitlement, puuid, region

    def auth(self):
        return self.get_needs(self.username, self.password)
