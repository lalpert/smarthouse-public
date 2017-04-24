from datetime import datetime, timedelta, date
from collections import defaultdict
import traceback

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flaskext.mysql import MySQL

import database_setup
from thermostat import Thermostat
from passwords import *

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

def median():
    query = """
    SELECT x.seconds_taken from crosswords x, crosswords y
    WHERE WEEKDAY(x.date) = %d
    GROUP BY x.val
    HAVING SUM(SIGN(1-SIGN(y.val-x.val)))/COUNT(*) > .5
    LIMIT 1
    """
    result = {}
    for day in range(7):
        day_query = query % day
        cursor = mysql.connect().cursor()
        cursor.execute(query)

        try:
            cursor.execute(query)
            data = cursor.fetchall()
            result[day] = data
        except mysql.connector.Error as e:
            print e
            print traceback.format_exc()
            result[day] = -1
    return result
    
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

    try:
        cursor.execute(query)
        data = cursor.fetchall()
    except mysql.connector.Error as e:
        print e
        print traceback.format_exc()
        data = []
        
    raw_graph_data = get_graph_data()
    print "data", raw_graph_data
    graph_data = defaultdict(list)

    for (day_name, date, seconds) in raw_graph_data:
        graph_data[day_name].append((date.isoformat(), seconds))

    print "graph_data", graph_data

    all_days = []
    for row in data:
        day_name = row[0]
        
        d = {
            "day": day_name,
            "num_complete": row[1],
            "avg_time": format_time(row[2]),
            "best_time": format_time(row[3]),
            "num_wrong": int(round(row[4])),
            "median_time":  format_time(get_median(graph_data[day_name]))
            }
        all_days.append(d)


    return render_template('crossword.html', table_data=all_days, graph_data=graph_data)


    for (day_name, date, seconds) in raw_graph_data:
        graph_data[day_name].append((date.isoformat(), seconds))

def get_median(day_list):
    times = [t[1] for t in day_list]
    return median(times)



def median(lst):
    sorted_lst = sorted(lst)
    lst_len = len(lst)
    index = (lst_len - 1) // 2

    if lst_len % 2 == 1:
        return sorted_lst[index]
    else:
        return (sorted_lst[index] + sorted_lst[index + 1])/2.0

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
therm = Thermostat("https://agent.electricimp.com/Zik1cm6CNOlE", wunderground_url, IMP_PASSWORD)

### Thermostat

@app.route("/api/thermostat/status", methods=['GET'])
def thermostat_status():
    return jsonify(inside = therm.inside_temp(), outside = therm.outside_temp(), setpoint = therm.setpoint(), heat_on = therm.heat_on())

@app.route("/api/thermostat/set", methods=['POST'])
def set_temp():
    req_data = request.get_json()
    if req_data and "temp" in req_data:
        therm.set_override(req_data["temp"], req_data.get("time_minutes"))
        return jsonify(inside = therm.inside_temp(), outside = therm.outside_temp(), setpoint = therm.setpoint(), heat_on = therm.heat_on())
    else:
        return jsonify(status = "ERROR", cause = "JSON argument %s was invalid" % req_data)

@app.route("/api/thermostat/update", methods=['POST'])
def set_temp_password():
    req_data = request.get_json()
    if req_data and "temp" in req_data and req_data["password"] == IMP_PASSWORD:
        therm.set_override(req_data["temp"], req_data.get("time_minutes"))
        return jsonify(inside = therm.inside_temp(), outside = therm.outside_temp(), setpoint = therm.setpoint(), heat_on = therm.heat_on())
    else:
        return jsonify(status = "ERROR", cause = "JSON argument %s was invalid" % req_data)
    

if __name__ == "__main__":
    # TODO: put it behind a real webserver at some point
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop
    from trequests import setup_session
    setup_session()
    #from yourapplication import app


    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(80)
    IOLoop.instance().start()
