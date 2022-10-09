from pynput import keyboard
import subprocess
from datetime import datetime
import os
from variables import acc_id
import configparser
config = configparser.ConfigParser()		
parentdir = os.path.dirname(__file__)
os.path.abspath(os.path.join(parentdir, os.pardir))
config.read("/".join([parentdir,"config.ini"]))

acc = config[f'ACCOUNT{acc_id+1}']
username = acc['riot_username']
password = acc['password']

def LogIn():

    COMBINATIONS = [
        { keyboard.Key.shift, keyboard.Key.ctrl },
    ]

    current = set()

    def execute():
        print(f'[{datetime.now().strftime("%H:%M:%S")}] Game launched')
        RIOTCLIENT_PATH = r'G:\Riot Games\Riot Client\RiotClientServices.exe' # <-- modify with the path of 'RiotClientServices.exe'
        subprocess.Popen(RIOTCLIENT_PATH)
        print(f'[{datetime.now().strftime("%H:%M:%S")}] Riot Client started')
        import win32api
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        win32api.Sleep(6000)
        shell.SendKeys(username)
        shell.SendKeys("{TAB}")
        shell.SendKeys(password)
        shell.SendKeys("{ENTER}")
        import sys
        sys.exit()


    def xlate(key):
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            return keyboard.Key.ctrl
        if key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
            return keyboard.Key.shift
        return key

    def on_release(key):
        key = xlate(key)
        if key in current:
            current.remove(key)

    def on_press(key):
        key = xlate(key)
        if any([key in COMBO for COMBO in COMBINATIONS]):
            current.add(key)
            if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
                execute()

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()