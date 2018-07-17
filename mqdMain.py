from merakiApi import *

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/who')
def who():
    r = getGroup()
    return str(r)

@app.route('/group')
def group():
    r = getGroup()
    html = "The Group Name is: " + str(r[0]['name']) + "<br>" + "The Group ID is: " + str(r[0]['id'])
    return html

# @app.route('/SportPoll/vote/<Sport>')
# def SportPoll(Sport=None):
#     t = DataFrame({'sport':[str(Sport)]})
#     try:
#         SportList = DataFrame.from_csv('data/SportPoll.csv')
#         SportList = SportList.append(t, ignore_index=True)
#     except:
#         SportList = t
#     SportList.to_csv('data/SportPoll.csv')
#     r = DataFrame(SportList['sport'].value_counts())
#     return r.to_html(border=0)
