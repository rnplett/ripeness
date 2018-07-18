from merakiApi import *
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

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
    summary = DataFrame(clientDevices["FullName"].value_counts())
    summary.columns = ["Device_Count"]

    return summary.to_html(border=0)

@app.route('/group')
def group():
    r = getGroup()
    html = "The Group Name is: " + str(r[0]['name']) + "<br>" + "The Group ID is: " + str(r[0]['id'])
    return html
