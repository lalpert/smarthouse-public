import requests
import time
class Thermostat(object):
	last_outside_fetch = -1
	outside_cache = None
	OUTSIDE_REFRESH_SECS = 60 * 15

	last_inside_fetch = -1
	inside_cache = None
	INSIDE_REFRESH_SECS = 30

	def __init__(self, imp_url, wunderground_url):
		self.imp_url = imp_url
		self.wunderground_url = wunderground_url

	def therm_info(self):
		if self.inside_cache == None or time.time() - self.last_inside_fetch > self.INSIDE_REFRESH_SECS:
			print "Downloading temp from imp"
			response = requests.get(self.imp_url + "/status")
			self.inside_cache = response.json()
			self.last_inside_fetch = time.time()
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