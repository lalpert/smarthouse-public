#!/bin/bash

# This script runs all commands needed to get "smarthouse" up and running on a Linux server. 
# It clones the git repos, downloads needed packages, and sets up the database.
# Run script with sudo. Script will prompt for MySQL password.

# Get newest version of packages and install git and pip
apt-get update
apt-get install git
apt-get install python-pip

# Install casperjs and phantomjs for the crossword scraping
apt-get install phantomjs
git clone git://github.com/n1k0/casperjs.git
ln -sf `pwd`/casperjs/bin/casperjs /usr/local/bin/casperjs

# Clone public and private smarthouse repos (private will fail if you don't have access)
git clone https://github.com/lalpert/smarthouse-public.git
git clone https://github.com/lalpert/smarthouse-private.git

# Make symlinks so public code can access private passwords
ln -s `pwd`/smarthouse-private/passwords.py `pwd`/smarthouse-public/webpage/
ln -s `pwd`/smarthouse-private/passwords.js `pwd`/smarthouse-public/server/

# Install mysql and related tools
apt-get install mysql-server
apt-get install mysql-client
apt-get install libmysqlclient-dev
apt-get install python-mysqldb
apt-get install python-dev

# Install necessary Python packages
pip install -r smarthouse-public/requirements.txt

# Set up database
mysql -u root -p -e "
CREATE DATABASE smarthouse;
use smarthouse;

CREATE TABLE crosswords(
 id INT NOT NULL AUTO_INCREMENT,
 date DATE NOT NULL,
 seconds_taken INT NOT NULL,
 num_wrong INT NOT NULL,
 PRIMARY KEY(id)
 );"

