from datetime import datetime, timedelta, date
from collections import defaultdict
import traceback

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flaskext.mysql import MySQL

import database_setup
from Thermostat import Thermostat

mysql = MySQL()

app = Flask(__name__)
# Add the database password, username, etc
database_setup.add_config_params(app)
mysql.init_app(app)

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/thermostat")
def thermostat():
    return render_template('thermostat.html')

@app.route("/garage")
def garage():
    return render_template('garage.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

def format_time(num_seconds):
    rounded_seconds = int(round(num_seconds))
    delta = timedelta(seconds=rounded_seconds)
    return str(delta)

def get_graph_data():
    query = """
        SELECT 
        DAYNAME(date) as day_name,
        date,    
        seconds_taken
        FROM crosswords
        ORDER BY date;
    """
    cursor = mysql.connect().cursor()
    cursor.execute(query)
    data = cursor.fetchall()

    return data
    
@app.route("/crossword")
def crossword():
    query = """
        SELECT 
        DAYNAME(date) as day_name,
        COUNT(id),
        AVG(seconds_taken),
        MIN(seconds_taken),
        AVG(num_wrong),
        WEEKDAY(date) as day_num
        FROM crosswords
        GROUP BY DAYNAME(date)
        ORDER BY WEEKDAY(date);"""

    cursor = mysql.connect().cursor()
    cursor.execute(query)

    try:
        cursor.execute(query)
        data = cursor.fetchall()
    except mysql.connector.Error as e:
        print e
        print traceback.format_exc()
        data = []
        

    all_days = []
    for row in data:
        d = {
            "day": row[0],
            "num_complete": row[1],
            "avg_time": format_time(row[2]),
            "best_time": format_time(row[3]),
            "num_wrong": int(round(row[4])),
            }
        all_days.append(d)

    data = get_graph_data()
    print "data", data
    graph_data = defaultdict(list)

    for (day_name, date, seconds) in data:
        graph_data[day_name].append((date.isoformat(), seconds))

    print "graph_data", graph_data

    return render_template('crossword.html', table_data=all_days, graph_data=graph_data)

def dataForDay(day):
    query = """
        SELECT * 
        FROM crosswords
        WHERE WEEKDAY(date) == %s""" % day

@app.route("/api/crosswords", methods=['POST'])
def add_crossword():
    print "request", request
    print request.form
    date = request.form['date']
    time_string = request.form['time']
    num_wrong = request.form['num_wrong']

    cxn = mysql.connect()
    cursor = cxn.cursor()

    # First check if date is already in db. If so, don't add it again.
    query = "SELECT * FROM crosswords WHERE date = %s"
    data = (date,)
    cursor.execute(query, data)
    result = cursor.fetchone()
    print "result", result
    if result:
        print "ALREADY HAVE STATS FOR", date, result
        return "nop"

    # Parse time string like 1:02:58 into a number of seconds
    t = datetime.strptime(time_string,"%H:%M:%S")
    time = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second).total_seconds()
    data = (date, time, num_wrong)

    query = """
    INSERT INTO crosswords (date,seconds_taken,num_wrong) 
    VALUES(%s, %s, %s);
    """

    cursor.execute(query, data)
    cxn.commit()
    return "done"

wunderground_url = "http://api.wunderground.com/api/78cca52724e6929e/conditions/q/CA/Redwood_City.json"
therm = Thermostat("https://agent.electricimp.com/Zik1cm6CNOlE", wunderground_url)
### Thermostat
# Operations:
# -- Schedule override
# -- Set temp
# -- Get status (inside, outside, etc...)
@app.route("/api/thermostat/status", methods=['GET'])
def thermostat_status():
    return jsonify(inside = therm.inside_temp(), outside = therm.outside_temp())

if __name__ == "__main__":
    # TODO: put it behind a real webserver at some point
    app.run(host='0.0.0.0', port=80, threaded=True, debug=True)
