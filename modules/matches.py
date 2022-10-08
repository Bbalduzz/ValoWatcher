from os import kill
from modules.player import get_player_id
from requests import get

def GetMatches(needs):
    puuid = needs[2]
    entitlement = needs[1]
    token = needs[0]
    region = needs[3]
    headers = {
        # 'User-Agent': 'RiotClient/58.0.0.4640299.4552318 rso-auth (Windows;10;;Professional, x64)',
        'X-Riot-Entitlements-JWT': entitlement,
        'Authorization': f'Bearer {token}',
        'X-Riot-ClientPlatform': 'ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9'
    }
    params = {
        'startIndex': 0,
        'endIndex': 10,
        'queue': 'competitive' # can be one of null, competitive, custom, deathmatch, ggteam, newmap, onefa, snowball, spikerush, or unrated
    }

    r = get(f'https://pd.{region}.a.pvp.net/mmr/v1/players/{puuid}/competitiveupdates', headers=headers, params=params).json()
    matches = r['Matches']

    match_ids = [matches[n]['MatchID'] for n in range(len(matches))]
    matches_results = get_matches_results(needs, match_ids)

    competitive_matches_results = []
    for n in range(len(matches)):
        rank_after = matches[n]['TierAfterUpdate']
        rank_earnings = matches[n]['RankedRatingEarned']
        comp_game = [rank_after, rank_earnings]
        competitive_matches_results.append(comp_game)

    return [matches_results, competitive_matches_results]

def get_matches_results(needs, match_ids: list):
    puuid = needs[2]
    entitlement = needs[1]
    token = needs[0]
    region = needs[3]
    playerID = get_player_id(needs)
    headers = {
        # 'User-Agent': 'RiotClient/58.0.0.4640299.4552318 rso-auth (Windows;10;;Professional, x64)',
        'X-Riot-Entitlements-JWT': entitlement,
        'Authorization': f'Bearer {token}',
        'X-Riot-ClientPlatform': 'ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9'
    }
    matches_results = [] # win or lose
    agents_played = []
    kda = []
    for match_id in match_ids:
        r = get(f'https://pd.{region}.a.pvp.net/match-details/v1/matches/{match_id}', headers=headers).json()
        for n in range(len(r['players'])):
            if r['players'][n]['gameName'] == playerID.split('#')[0]:
                team_color =r['players'][n]['teamId']
                id_agent_played =r['players'][n]['characterId']
                kills, deaths, assists = r['players'][n]['stats']['kills'], r['players'][n]['stats']['deaths'], r['players'][n]['stats']['assists']
        if r['teams'][0]['teamId'] == team_color:
            if r['teams'][0]['won'] == True:
                match_result = 'win'
            else:
                match_result = 'lost'
        else:
            if r['teams'][1]['won'] == True:
                match_result = 'win'
            else:
                match_result = 'lost'
        matches_results.append(match_result)
                
        r = get(f'https://valorant-api.com/v1/agents/{id_agent_played}').json()
        agent_played = r['data']['displayName']
        
        agents_played.append(agent_played)
        kda.append([kills, deaths, assists])
    

    return matches_results, agents_played, kda
