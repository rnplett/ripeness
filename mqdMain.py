from merakiApi import *
from flask import Flask, render_template, abort
import pandas as pd

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    # Get Directory data
    d = pd.read_csv("data/directory.csv")
    d.columns = ["client","FullName"]

    # Get Client data from Meraki API
    g = getGroup()
    c = getClients(g[0]['id'])
    c = c.loc[:,["description","mac","serial"]]
    c.columns = ["client","gatewayMac","gatewaySN"]

    # Add directory data to the Client data for display.
    clientDevices = c.merge(d,'left')
    people = DataFrame(clientDevices["FullName"].value_counts())
    people["Description"] = people.index
    people.index = [s.replace(' ','') for s in people.index]
    people.columns = ["Device_Count","FullName"]

    people.to_json("data/people.json", orient="index")

    return render_template('home.html', people=json.loads(people.to_json(orient="index")))

@app.route('/person/<name>')
def person(name):
    people = pd.read_json("data/people.json")
    person = people[name]
    # if not person:
    #     abort(404)
    return render_template('person.html', person=person)

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/who')
def who():
    # Get Directory data
    d = pd.read_csv("data/directory.csv")
    d.columns = ["client","FullName"]

    # Get Client data from Meraki API
    g = getGroup()
    c = getClients(g[0]['id'])
    c = c.loc[:,["description","mac","serial"]]
    c.columns = ["client","gatewayMac","gatewaySN"]

    # Add directory data to the Client data for display.
    clientDevices = c.merge(d,'left')
    people = DataFrame(clientDevices["FullName"].value_counts())
    people.columns = ["Device_Count"]

    return people.to_html(border=0)

@app.route('/group')
def group():
    r = getGroup()
    html = "The Group Name is: " + str(r[0]['name']) + "<br>" + "The Group ID is: " + str(r[0]['id'])
    return html
