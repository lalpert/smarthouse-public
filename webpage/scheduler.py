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

DEFAULT_CONFIG = {"schedule": [
                    {"hr": WAKEUP_HR, "temp": AWAY_TEMP, "name": "wakeup"}, 
                    {"hr": WORK_HR, "temp": AWAY_TEMP, "name": "work"},
                    {"hr": HOME_HR, "temp": HOME_TEMP, "name": "home"},
                    {"hr": BED_HR, "temp": NIGHT_TEMP, "name": "bed"}],
                  "overrides": [{"temp": -1, "expires": -1, "starts": -1}]
                 }

CONFIG_LOC = "config.json"


class Scheduler(object):
    def __init__(self, temp_update_callback):
        self.callback = temp_update_callback

    def get_config(self):
        data = cfgsrv.deserialize(CONFIG_LOC)

        if data:
            return data
        else:
            print "writing default"
            cfgsrv.serialize(DEFAULT_CONFIG, CONFIG_LOC)
            return DEFAULT_CONFIG


    def hour_in_range(self, start, end):
        hour = datetime.datetime.now().hour
        if start > end:
            return hour >= start or hour <= end
        else:
            return start <= hour <= end

    def update_temp(self):
        print self.get_config()
        schedule = self.get_config()["schedule"]
        overrides = self.get_config()["overrides"]
        if not self.update_based_on_override(overrides):
            self.update_based_on_schedule(schedule)

    def now(self):
        return time.time()

    def update_based_on_override(self, overrides):
        now = self.now()
        for override in overrides:
            if override["expires"] > now and override["starts"] < now:
                print "running override", override
                self.callback(override["temp"])
                return True
            else:
                print "override doesn't apply"

        return False

    def add_override(self, temp, time_minutes):
        current_config = self.get_config()
        now = self.now()
        current_config["overrides"] = [{"temp": temp, "starts": now, "expires": now + time_minutes * 60}]
        cfgsrv.serialize(current_config, CONFIG_LOC)
        self.update_temp()


    def update_based_on_schedule(self, schedule):
        looped_config = schedule + [schedule[0]]
        for i in range(len(looped_config) - 1):
            start = looped_config[i]
            end = looped_config[i+1]
            if self.hour_in_range(start['hr'], end['hr']):
                self.callback(start['temp'])
            