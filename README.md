Smarthouse
==========

A smart house for dumb people

Check it out at 735roosevelt.com

- Displays current temperature in our house and controls the thermostat 
- Displays whether garage door is open or closed, and can open/close garage door
- Displays our stats for the New York Times crossword puzzle

The electric imp code that interacts with the thermostat and garage door aren't in this repo because it contains passwords and sensitive URLs. If you're interested in that part, contact us or read about it here:
http://rcoh.svbtle.com/how-i-automated-my-garage-door
http://rcoh.svbtle.com/make-your-own-internet-connected-thermostat

Setup
=====

To set up on a server, download the setup script and run 
`sudo ./setup.sh`
This will download the repository and other needed packages.

To run the website on port 80, run
`sudo python smarthouse-public/webpage/app.py`
