import datetime
import time
import requests
import cfgsrv
import json 


AWAY_TEMP = 60
NIGHT_TEMP = 60
HOME_TEMP = 60

WAKEUP_HR = 8
WORK_HR = 10
HOME_HR = 19
BED_HR = 23

DEFAULT_CONFIG = [
        {"hr": WAKEUP_HR, "temp": AWAY_TEMP, "name": "wakeup"}, 
        {"hr": WORK_HR, "temp": AWAY_TEMP, "name": "work"},
        {"hr": HOME_HR, "temp": HOME_TEMP, "name": "home"},
        {"hr": BED_HR, "temp": NIGHT_TEMP, "name": "bed"}
        ]

SET_URL = "https://agent.electricimp.com/Zik1cm6CNOlE/set"
CONFIG_LOC = "config.json"

def get_config():
    data = cfgsrv.deserialize(CONFIG_LOC)

    if data:
        return data
    else:
        cfgsrv.serialize(DEFAULT_CONFIG, CONFIG_LOC)
        return DEFAULT_CONFIG

def set_temp(temp, password):
    arg = {"temp": temp, "password": password}
    result = requests.post(SET_URL, json.dumps(arg))
    print(result.json(), str(datetime.datetime.now()))


def hour_in_range(start, end):
    hour = datetime.datetime.now().hour
    if start > end:
        return hour >= start or hour <= end
    else:
        return start <= hour <= end

def update_temp(password):
    config = get_config()
    looped_config = config + [config[0]]
    for i in range(len(looped_config) - 1):
        start = looped_config[i]
        end = looped_config[i+1]
        if hour_in_range(start['hr'], end['hr']):
            set_temp(start['temp'], password)
            return

if __name__ == "__main__":    
    import sys
    password = sys.argv[1]
    while 1:
        try:
            update_temp(password)
        except Exception as e:
            print("Error updating temperature", e)
        finally:
            time.sleep(60)

