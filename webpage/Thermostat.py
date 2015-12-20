import requests
import time
from scheduler import Scheduler
class Thermostat(object):
    last_outside_fetch = -1
    outside_cache = None
    OUTSIDE_REFRESH_SECS = 60 * 15
    
    last_inside_fetch = -1
    inside_cache = None
    INSIDE_REFRESH_SECS = 30
    
    ## TODO: update last_inside_fetch on mutation so it updates without latency
    
    def __init__(self, imp_url, wunderground_url, password):
    	self.imp_url = imp_url
    	self.wunderground_url = wunderground_url
    	self.password = password
    	self.scheduler = Scheduler(self.set_temp)
    
    def therm_info(self):
    	if self.inside_cache == None or time.time() - self.last_inside_fetch > self.INSIDE_REFRESH_SECS:
    		print "Downloading temp from imp"
    		response = requests.get(self.imp_url + "/status")
    		self.inside_cache = response.json()
    		self.last_inside_fetch = time.time()
    		print "Got temp from imp"
    	return self.inside_cache
    
    def inside_temp(self):
    	return self.therm_info()['temp']
    
    def setpoint(self):
    	return self.therm_info()['setpoint']
    
    def heat_on(self):
    	return bool(self.therm_info()['heat'])
    
    def outside_temp(self):
    	if self.outside_cache == None or time.time() - self.last_outside_fetch > self.OUTSIDE_REFRESH_SECS:
    		print "Downloading temp from wunderground"
    		response = requests.get(self.wunderground_url)
    		self.last_outside_fetch = time.time()
    		self.outside_cache = response.json()['current_observation']['temp_f']
    
    	return self.outside_cache
    
    def set_override(self, temp, time_minutes):
    	print "Setting temperature to ", temp, "for", time_minutes
        if time_minutes == None:
            time_minutes = 60
    	self.scheduler.add_override(temp, time_minutes)
    	self.last_inside_fetch = -1
    
    def set_temp(self, temp):
        requests.post(self.imp_url + "/set", json = {"password": self.password, "temp": str(temp)})
    
