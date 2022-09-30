"""
Extracts all Chrome cookies found on host in a JSON file
"""
import datetime as dt
import getpass
import json
import os
import signal
import subprocess
import sys
import time
from typing import Any, Dict, Tuple

import requests
import websocket


def get_paths() -> Tuple[str, str]:
    """Gets Chrome installation and user data directories"""
    chrome_dir = None

    if sys.platform.startswith('win'):
        locations = (
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            rf'C:\Users\{getpass.getuser()}\AppData\Local\Google\Chrome\Application\chrome.exe',
        )

        for location in locations:
            if os.path.isfile(location):
                chrome_dir = f'"{location}"'
                break

        user_data_dir = r'%LOCALAPPDATA%\Google\Chrome\User Data'

    elif sys.platform.startswith('darwin'):
        chrome_dir = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        user_data_dir = '$HOME/Library/Application Support/Google/Chrome'

    elif sys.platform.startswith('linux'):
        chrome_dir = 'google-chrome'
        user_data_dir = '$HOME/.config/google-chrome/'

    else:
        raise RuntimeError(f'Cannot work with OS {sys.platform}')

    if chrome_dir is None:
        raise RuntimeError('No installation of Chrome detected.')

    return chrome_dir, user_data_dir


def run_chrome_cmd(chrome_dir: str, user_data_dir: str) -> subprocess.Popen:
    """Spawns a headless Chrome instance"""
    chrome_cmd = (
        f'{chrome_dir} --user-data-dir="{user_data_dir}" https://www.google.com --headless --remote-debugging-port=9222'
    )
    process = subprocess.Popen(chrome_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(6)
    return process


def get_cookies() -> Dict[str, Any]:
    """Extracts cookies from Chrome instance"""
    websocket_url = requests.get('http://localhost:9222/json').json()[0].get('webSocketDebuggerUrl')
    ws = websocket.create_connection(websocket_url)

    ws.send(json.dumps({'id': 1, 'method': 'Network.getAllCookies'}))
    result = ws.recv()

    ws.close()
    return json.loads(result)['result']['cookies']


def kill_chrome_process(chrome_proc: subprocess.Popen) -> None:
    """Kills spawned Chrome instance"""
    if sys.platform.startswith('win'):
        os.kill(chrome_proc.pid + 1, signal.SIGTERM)
    else:
        os.kill(chrome_proc.pid + 1, signal.SIGKILL)


if __name__ == '__main__':
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        time_now = dt.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
        output = f'{dir_path}/cookies_{time_now}.json'

        chrome_directory, user_data_directory = get_paths()
        chrome_process = run_chrome_cmd(chrome_directory, user_data_directory)

        cookies = get_cookies()
        time.sleep(1)
        kill_chrome_process(chrome_process)

        with open(output, 'w', encoding='utf-8') as f:
            f.write(json.dumps(cookies, indent=4, separators=(',', ': '), sort_keys=True))

    except Exception as err:
        raise
    else:
        print('Done!')
    finally:
        time.sleep(2)
