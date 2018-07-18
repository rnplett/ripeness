import datetime, re, os
from pandas import Series, DataFrame
from flask import Flask
from inputs.settings import *
import requests
import json

def getGroup():
    url = "https://api.meraki.com/api/v0/organizations"

    headers = {
       'cache-control': "no-cache",
       'x-cisco-meraki-api-key': MERAKI_KEY
       }
    payload = ""
    response = requests.request("GET", url, data=payload, headers=headers)

    r = json.loads(response.text)

    return r

def getDevices(oid):
    url = "https://dashboard.meraki.com/api/v0/organizations/" + str(oid) + "/inventory"

    headers = {
        'x-cisco-meraki-api-key': MERAKI_KEY,
        'Content-Type': 'application/json'
       }
    payload = ""
    response = requests.request("GET", url, data=payload, headers=headers)

    r = json.loads(response.text)

    return r

def getClients(oid):

    r = getDevices(oid)
    h = []

    for i in r:
        url = "https://dashboard.meraki.com/api/v0/devices/" + str(i['serial']) + "/clients?timespan=900"
        headers = {
            'x-cisco-meraki-api-key': MERAKI_KEY,
            'Content-Type': 'application/json'
            }
        payload = ""
        response = requests.request("GET", url, data=payload, headers=headers)
        r = json.loads(response.text)
        h = h + r

    return h
