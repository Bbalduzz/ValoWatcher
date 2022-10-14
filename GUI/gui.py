# local imports #
import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
import variables

# account switcher imports #
import os
import configparser
config = configparser.ConfigParser()		
parentdir = os.path.dirname(__file__)
os.path.abspath(os.path.join(parentdir, os.pardir))
config.read("/".join([parentdir,"config.ini"]))

# gui imports
from rich.table import Table
from rich.layout import Layout
from rich.align import Align
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
from rich.rule import Rule
from rich import print, box
from utils import get_terminal_width, retrive_rank
console = Console()
def clean():
    os.system('cls||clear')

def print_banner() -> Panel:
    width = get_terminal_width()
    height = 10
    banner = '''\

██╗   ██╗ █████╗ ██╗      ██████╗ ██╗    ██╗ █████╗ ████████╗ ██████╗██╗  ██╗███████╗██████╗ 
██║   ██║██╔══██╗██║     ██╔═══██╗██║    ██║██╔══██╗╚══██╔══╝██╔════╝██║  ██║██╔════╝██╔══██╗
██║   ██║███████║██║     ██║   ██║██║ █╗ ██║███████║   ██║   ██║     ███████║█████╗  ██████╔╝
╚██╗ ██╔╝██╔══██║██║     ██║   ██║██║███╗██║██╔══██║   ██║   ██║     ██╔══██║██╔══╝  ██╔══██╗
 ╚████╔╝ ██║  ██║███████╗╚██████╔╝╚███╔███╔╝██║  ██║   ██║   ╚██████╗██║  ██║███████╗██║  ██║
  ╚═══╝  ╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

'''

    banner_small = """\
 █ █ ▄▀▄ █   ▄▀▄ █   █ ▄▀▄ ▀█▀ ▄▀▀ █▄█ ██▀ █▀▄
 ▀▄▀ █▀█ █▄▄ ▀▄▀ ▀▄▀▄▀ █▀█  █  ▀▄▄ █ █ █▄▄ █▀▄
"""

    if width < 90:
        banner = banner_small
        height = 5

    panel = Panel(
        Align(
            Text(banner, justify="center", style="blue"),
            vertical="middle",
            align="center",
        ),
        width=width,
        height=height,
        subtitle="by Balduzz (https://github.com/Bbalduzz)",
    )

    return panel

def show_player_infos() -> Panel:
    info_sub_title = Panel(
        Align.center(Text(f'Region: {variables.needs[3].upper()}\nRank: {retrive_rank()[0]}\nMMR: {variables.mmr}', justify="center", style='bold')),
        box=box.ROUNDED,
        padding=(1, 2),
        title="[b red]Info",
        border_style="green",
    )
    return info_sub_title

def show_player_progress() -> Panel:
    info_sub_title = Panel(
        Align.center(Text(f'Level: {variables.player_level} \nXP: {variables.player_xp}', style='bold')),
        box=box.ROUNDED,
        padding=(1, 2),
        title="[b red]Progress",
        border_style="green",
    )
    return info_sub_title

def show_player_balances() -> Panel:
    info_sub_title = Panel(
        Align.center(Text(f'VP: {variables.player_valorantpoints} VP \nRadiante: {variables.player_radianite} R\nFree Agents: 0', style='bold')),
        box=box.ROUNDED,
        padding=(1, 2),
        title="[b red]Balances",
        border_style="green",
    )
    return info_sub_title

def table_shop():  
    table_one = Table(box=box.HORIZONTALS, title='Daily Shop', expand=True, show_header=True, header_style='bold #2070b2')
    table_one.add_column('Skin', justify='left')
    table_one.add_column('Price', justify='center')
    for item in variables.store:
        table_one.add_row(item, str(variables.full_store[item]))
    if variables.nightmarket_store == 'NONE':
        pass
    else:
        table_two = Table(box=box.HORIZONTALS, title='Night Market', expand=True, show_header=True, header_style='bold #2070b2')
        table_two.add_column('Offer', justify='left')
        table_two.add_column('Price', justify='center')
        for item in variables.nightmarket_store:
            table_two.add_row(item, str(variables.nightmarket_store[item]))

    store_table = Table(box=None, expand=True, show_header=True, header_style='bold #2070b2')
    if variables.nightmarket_store == 'NONE':
        store_table.add_row(table_one)
    else: store_table.add_row(table_one, table_two)

    return store_table

def show_shop() -> Panel:
    shop_table_panel = Panel(
        table_shop(),
        box=box.ROUNDED,
        padding=(1, 2),
        title="[b red] Shop",
        border_style="blue",
    )

    return shop_table_panel

def match_table(index) -> Table:
    match_table = Table(box=None, expand=True, show_header=False, show_edge=False, pad_edge=True)
    match_table.add_row(f"{variables.agets_played[int(index)]}   KD: {round(variables.kills_deaths_assists[int(index)][0]/variables.kills_deaths_assists[int(index)][1], 2)}  KDA: {variables.kills_deaths_assists[int(index)]}  RR: {variables.competitive_matches_results[int(index)][1]}  Result: {variables.winorlost[int(index)]} ")

    return match_table

def single_match_stat(index) -> Panel:
    if variables.winorlost[int(index)] == 'lost':
        border_color = 'red'
    else:
        border_color = 'blue'
    single_match = Panel(
        Align.center(match_table(index)),
        box=box.ROUNDED,
        border_style=border_color
    )
    return single_match

def matches_loop() -> Layout:
    matches_layout = Layout(name='matches')
    matches_layout.split(
        Layout(name='rank', size=3),
        Layout(name=f'match0', size=3),
        Layout(name=f'match1', size=3),
        Layout(name=f'match2', size=3),
        Layout(name=f'match3', size=3),
        Layout(name=f'match4', size=3),
        Layout(name=f'match5', size=3),
        Layout(name=f'match6', size=3),
        Layout(name=f'match7', size=3),
        Layout(name=f'match8', size=3),
    )
    
    matches_layout['rank'].update(Align.center(f'Current Rank: [#{retrive_rank()[1]}]{retrive_rank()[0]}'))
    matches_layout[f'match0'].update(single_match_stat(0))
    matches_layout[f'match1'].update(single_match_stat(1))
    matches_layout[f'match2'].update(single_match_stat(2))
    matches_layout[f'match3'].update(single_match_stat(3))
    matches_layout[f'match4'].update(single_match_stat(4))
    matches_layout[f'match5'].update(single_match_stat(5))
    matches_layout[f'match6'].update(single_match_stat(6))
    matches_layout[f'match7'].update(single_match_stat(7))
    matches_layout[f'match8'].update(single_match_stat(8))

    
    return matches_layout
    

def show_matches_stat() -> Panel:
    matches_stats = Panel(
        matches_loop(),
        box=box.ROUNDED,
        padding=(1, 2),
        title="[b red] Matches",
        border_style="blue",
    )

    return matches_stats

def launcher_message() -> str:
    message = f'Lauch [b red]VALORANT[/b red] as [b red]{variables.playerID}[/b red]. Press [b red] SHIFT + L [/b red]to launch'
    return message
def show_laucher() -> Panel:
    launcher = Panel(
        Align.center(launcher_message()),
        box=box.ROUNDED,
        padding=(1, 2),
        title="[b red] Launcher",
        border_style="white",
    )

    return launcher

def MakeLayout() -> Layout:
    layout = Layout(name="root")
    layout.split(
        Layout(name="header", size=10), # title
        Layout(name="main", ratio=1), # main part -> more divisions inside
        Layout(name="footer", size=5), # footer -> Launcher
    )
    layout["main"].split_row(
        Layout(name="side"),
        Layout(name="body", ratio=2, minimum_size=100),
    )
    layout["side"].split(
        Layout(name="PROFILE", size=2),
        Layout(name="INFORMAZIONI"),
        Layout(name="SHOP", ratio=2),
    )
    layout["INFORMAZIONI"].split_row(
        Layout(name="infos"),
        Layout(name="progress"),
        Layout(name="balances"),
    )
    return layout

layout = MakeLayout()
layout["header"].update(print_banner())
layout["PROFILE"].update(Rule(title=f"[b red]{variables.playerID}[/b red]'s Profile", style='rule.line'))
layout["SHOP"].update(show_shop())
layout["infos"].update(show_player_infos())
layout['progress'].update(show_player_progress())
layout['balances'].update(show_player_balances())
layout['body'].update(show_matches_stat())
layout['footer'].update(show_laucher())

clean()
print(layout)
