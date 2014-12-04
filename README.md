Smarthouse
==========

A smart house for dumb people

- Displays current temperature in our house and controls thermostat 
- Displays whether garage door is open or closed, and can open/close garage door
- Displays our stats for the New York Times crossword puzzle

The electric imp code that interacts with the thermostat and garage door aren't in this repo because it contains passwords and sensitive URLs. If you're interested in that part, contact us or read about it here:
http://rcoh.svbtle.com/how-i-automated-my-garage-door
http://rcoh.svbtle.com/make-your-own-internet-connected-thermostat

Setup
=====

To run on a server, you'll need to install mysql and some related tools:
```
sudo apt-get install mysql-server
sudo apt-get install mysql-client
sudo apt-get install libmysqlclient-dev
sudo apt-get install python-mysqldb
sudo apt-get install python-dev
```

Then install the python packages needed:
```
pip install -r requirements.txt
```

To set up the database:
```
CREATE DATABASE smarthouse;
use smarthouse;

CREATE TABLE crosswords(
 id INT NOT NULL AUTO_INCREMENT,
 date DATE NOT NULL,
 seconds_taken INT NOT NULL,
 num_wrong INT NOT NULL,
 PRIMARY KEY(id)
 );
```
