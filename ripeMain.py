from flask import Flask, render_template, abort, flash, request
from wtforms import Form, SubmitField, BooleanField, StringField, validators
from tradeObject import *
import json
from inputs.settings import *
from datetime import datetime, time, timedelta

class ReusableForm(Form):
    name = StringField('Enter Ticker:', validators=[validators.required()])

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        sym = request.form['name']
        pick = tradeObject()
        pick.daQuandl(sym)
        pick.createChart()
        sym_info = {}
        sym_info["chart"] = pick.chartURI
        sym_info["name"] = sym
        try:
            sym_info["describe"] = json.loads(pick.describe.to_json(orient="index"))
        except:
            sym_info["describe"] = "Error"
        return render_template('symbol.html', sym_info=sym_info)
    else:
        form = ReusableForm(request.form)
        print(form.errors)

    return render_template('home.html', form = form)

@app.route('/hello')
def hello():
    return 'Hello, World'


