from os import get_terminal_size
from platform import system
import variables
from requests import get
from rich.console import Console
c = Console()

def get_terminal_width() -> int:
    try:
        width, _ = get_terminal_size()
    except OSError:
        width = 80

    if system().lower() == "windows":
        width -= 1

    return width

def retrive_rank():
    last_rank = variables.competitive_matches_results[0][0]
    r = get('https://valorant-api.com/v1/competitivetiers').json()
    rank = r['data'][0]['tiers'][last_rank]['tierName']
    color = r['data'][0]['tiers'][last_rank]['color']
    return [rank, color]