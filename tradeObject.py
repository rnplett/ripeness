import pandas as pd
import quandl
import json
import sys
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_finance import candlestick2_ohlc
import matplotlib.colors
from io import BytesIO
import base64

from inputs.settings import *
from datetime import datetime, time, timedelta

class tradeObject(object):
    """
    object to standardize the definition and processing of a trading system.
    """

    def __init__(self, **kwargs):
        """
        :param id: master reference, has to be an immutable type
        :param kwargs: other attributes which will appear in list returned by attributes() method
        """

        attr_to_use=self.attributes()

        for argname in kwargs:
            if argname in attr_to_use:
                setattr(self, argname, kwargs[argname])
            else:
                print("Ignoring argument passed %s: is this the right kind of object? If so, add to .attributes() method" % argname)

     #other standard functions

    def attributes(self):
        ## should return a list of str here
        ## eg return ["thingone", "thingtwo"]
        return ["data","indicators"]

    def _name(self):
        return "Trading System object - "

    def __repr__(self):

        attr_list = self.attributes()
        if attr_list is NO_ATTRIBUTES_SET:
            return self._name()

        return self._name() + " ".join(
            ["%s: %s" % (attrname, str(getattr(self, attrname))) for attrname in attr_list
             if getattr(self, attrname, None) is not None])

    def daQuandl(self,sym='SPY'):
        quandl.ApiConfig.api_key = QUANDL_API_KEY
        base = datetime.today()
        dateList = [(base - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(0, 200)]
        try:
            p = quandl.get_table('SHARADAR/SEP', ticker=sym, date=dateList,
                                 qopts={"columns": ["ticker", "date", "open", "high", "low", "close"]})
            p.columns = ["Symbol", "datetime", "Open", "High", "Low", "Close"]
            p["Date"] = p["datetime"].apply(lambda x: x.strftime('%Y-%m-%d'))
        except:
            print("Quandl read error")
            p = ""
        self.data = p
        self.describe = p.tail()

    def addMAs(self):
        ma8 = 3


    def createChart(self):
        fig, ax = plt.subplots(figsize=(8, 4))
        candlestick2_ohlc(ax, self.data['Open'], self.data['High'], self.data['Low'], self.data['Close'], width=0.4)
        locs = [0,20,40,60,80,100,120,len(self.data)-1]
        plt.xticks(locs, self.data.loc[locs,'Date'])
        fig.autofmt_xdate()
        fig.tight_layout()
        figfile = BytesIO()
        fig.savefig(figfile, format='png')
        figfile.seek(0)
        figdata_png = base64.b64encode(figfile.getvalue()).decode('utf-8')
        self.chartURI = 'data:image/png;base64,{}'.format(figdata_png)

