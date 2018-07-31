from flask import Flask, render_template, abort, flash, request
from wtforms import Form, SubmitField, BooleanField, StringField, validators
import pandas as pd
import quandl
import json
from inputs.settings import *
from datetime import datetime, time, timedelta

quandl.ApiConfig.api_key = QUANDL_API_KEY

def getData(sym):
    base = datetime.today()
    dateList = [(base - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(0, 200)]
    p = ""
    try:
        p = quandl.get_table('SHARADAR/SEP', ticker=sym, date=dateList,
                             qopts={"columns": ["ticker", "date", "open", "high", "low", "close"]})
        p.columns = ["Symbol", "Date", "Open", "High", "Low", "Close"]
    except:
        print("Quandl read error")
    return p

class ReusableForm(Form):
    name = StringField('Enter Ticker:', validators=[validators.required()])

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    if request.method == 'POST':
        flash('Hello there')
        sym = 'SPY'
        p = getData(sym)
        sym_info = {}
        sym_info["name"] = sym
        try:
            sym_info["describe"] = p.describe().to_json()
        except:
            sym_info["describe"] = "Error"
        return render_template('symbol.html', sym_info=sym_info)
    else:
        form = ReusableForm(request.form)
        print(form.errors)

    return render_template('home.html', form = form)

@app.route('/entry/<sym>')
def entry(sym):
    p = getData(sym)
    sym_info = {}
    sym_info["name"] = sym
    try:
        sym_info["describe"] = p.describe().to_json()
    except:
        sym_info["describe"] = "Error"
    return render_template('symbol.html', sym_info=sym_info)

@app.route('/hello')
def hello():
    return 'Hello, World'


