from flask import Flask
import cfgsrv
import pullups

app = Flask(__name__)
config = cfgsrv.dict_wrapping("config.json")

@app.route("/temp_update/<name>/<newtime>")
def temp_update(name, newtime):
    config.load()
    for item in config:
        if item['name'] == name:
            item['hr'] = int(newtime)
    config.save()
    return "OK"

# Add a new person to the "database" (POST)
@app.route("pullups/people")
def add_person():
    # get name
    pullups.add_person(name)

# Increment a person's pullups count (POST)
@app.route("/pullups/people/<name>/add_pullup")
def add_pullup():
    pullups.add_pullup(name)

if __name__ == "__main__":
    app.run(debug=True)

