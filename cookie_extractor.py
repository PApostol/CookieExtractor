import os, sys, subprocess, json, signal, time, requests, websocket, datetime

def get_paths():
    chrome_dir = None

    if sys.platform.startswith('win'):
        locations = (r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
                     r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                     r'C:\Users\{0}\AppData\Local\Google\Chrome\Application\chrome.exe'.format(os.environ['username'].lower()))

        for location in locations:
            if os.path.isfile(location):
                chrome_dir = '"'+location+'"'
                break

        user_data_dir = r'%LOCALAPPDATA%\Google\Chrome\User Data'

    elif sys.platform.startswith('darwin'):
        chrome_dir = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        user_data_dir = '$HOME/Library/Application Support/Google/Chrome'

    elif sys.platform.startswith('linux'):
        chrome_dir = 'google-chrome'
        user_data_dir = '$HOME/.config/google-chrome/'

    else:
        raise RuntimeError('Cannot work with OS ' + sys.platform)

    if chrome_dir is None:
        raise RuntimeError('No installation of Chrome detected.')

    return chrome_dir, user_data_dir


def run_chrome_cmd(chrome_dir, user_data_dir):
    chrome_cmd = '{0} --user-data-dir="{1}" https://www.google.com --headless --remote-debugging-port=9222'.format(chrome_dir, user_data_dir)
    process = subprocess.Popen(chrome_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(6)
    return process


def get_cookies():
    websocket_url = requests.get('http://localhost:9222/json').json()[0].get('webSocketDebuggerUrl')
    ws = websocket.create_connection(websocket_url)

    ws.send(json.dumps({"id": 1, "method": "Network.getAllCookies"}))
    result = ws.recv()

    ws.close()
    return json.loads(result)['result']['cookies']


def kill_chrome_process(chrome_process):
    if sys.platform.startswith('win'):
        os.kill(chrome_process.pid + 1, signal.SIGTERM)
    else:
        os.kill(chrome_process.pid + 1, signal.SIGKILL)


if __name__ == "__main__":
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        time_now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output = dir_path + '/cookies_' + time_now + '.json'

        chrome_dir, user_data_dir = get_paths()
        chrome_process = run_chrome_cmd(chrome_dir, user_data_dir)

        cookies = get_cookies()
        time.sleep(1)
        kill_chrome_process(chrome_process)

        with open(output, 'w') as f:
            f.write(json.dumps(cookies, indent=4, separators=(',', ': '), sort_keys=True))

    except Exception as err:
        raise err
    else:
        print('Done!')
    finally:
        time.sleep(2)
        sys.exit()