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
        self.describe = p.tail(1)

    def bollinger_bands(self, m, n):
        """

        :param df: pandas.DataFrame
        :param n:
        :return: pandas.DataFrame
        """
        MA = pd.Series(self.data['Close'].rolling(n, min_periods=n).mean())
        MSD = pd.Series(self.data['Close'].rolling(n, min_periods=n).std())
        b1 = MA + m * MSD
        B3 = pd.Series(b1, name='BBU_' + str(n))
        self.data = self.data.join(B3)
        b1 = MA - m * MSD
        B4 = pd.Series(b1, name='BBD_' + str(n))
        self.data = self.data.join(B4)
        return

    def keltner_channel(self, m, n):
        """Calculate Keltner Channel for given data.
        true range=max[(high - low), abs(high - previous close), abs (low - previous close)]

        :param df: pandas.DataFrame
        :param n:
        :return: pandas.DataFrame
        """
        KelChM = pd.Series(self.data['Close'].rolling(n, min_periods=n).mean(), name='KelChM')
        r1 = self.data['High'] - self.data['Low']
        r2 = (self.data['High'] - self.data['Close'].shift(1)).abs()
        r3 = (self.data['Low'] - self.data['Close'].shift(1)).abs()
        TR = pd.DataFrame({'r1': r1, 'r2': r2, 'r3': r3}).max(axis=1)
        ATR = pd.Series(TR.rolling(n, min_periods=n).mean())
        KelChU = pd.Series(KelChM + ATR * m, name='KelChU')
        KelChD = pd.Series(KelChM - ATR * m, name='KelChD')
        try:
            self.data = self.data.join(KelChM)
            self.data = self.data.join(KelChU)
            self.data = self.data.join(KelChD)
        except:
            self.data["KelChM"] = KelChM
            self.data["KelChU"] = KelChU
            self.data["KelChD"] = KelChD

        return

    def squeeze(self):
        self.bollinger_bands( 2, 20)
        self.keltner_channel( 1.5, 20)
        self.data = self.data.join(pd.Series((self.data["BBU_20"] < self.data["KelChU"]) & (self.data["BBD_20"] > self.data["KelChD"]), name='Squeeze'))
        return

    def squeezeWeekly(self):
        self.bollinger_bands( 2, 100)
        self.keltner_channel( 1.5, 100)
        self.data = self.data.join(pd.Series((self.data["BBU_20"] < self.data["KelChU"]) & (self.data["BBD_20"] > self.data["KelChD"]), name='SqueezeWeekly'))
        return

    def squeezeLen(self):
        l = 0
        for x in range(1, 26):
            if self.data["Squeeze"].iloc[-x]:
                l = l + 1
            else:
                break
        return l

    def squeezeLenWeekly(self):
        l = 0
        for x in range(1, 26):
            if self.data["SqueezeWeekly"].iloc[-x]:
                l = l + 1
            else:
                break
        return l

    def createChart(self):
        fig, ax = plt.subplots(figsize=(8, 4))

        candlestick2_ohlc(ax, self.data['Open'], self.data['High'], self.data['Low'], self.data['Close'], width=0.4)

        xs = len(self.data)
        locs = [0,20,40,60,80,100,120,xs-1]
        plt.xticks(locs, self.data.loc[locs,'Date'])

        a = self.data.sort_values('Date', ascending=False).reset_index(drop=True)

        ma = a.loc[0:8, 'Close'].mean()
        plt.hlines(ma, xs, xs + 1, colors="blue")
        plt.text(x = xs + 2, y = ma, s = "8", fontsize = 8, color='b')

        ma = a.loc[0:21, 'Close'].mean()
        plt.hlines(ma, xs, xs + 2, colors="blue")
        plt.text(x = xs + 3, y = ma, s = "21", fontsize = 8, color='b')

        ma = a.loc[0:50, 'Close'].mean()
        plt.hlines(ma, xs, xs + 4, colors="blue")
        plt.text(x = xs + 5, y = ma, s = "50", fontsize = 8, color='b')

        ma = a.loc[0:100, 'Close'].mean()
        plt.hlines(ma, xs, xs + 6, colors="blue")
        plt.text(x = xs + 7, y = ma, s = "100", fontsize = 8, color='b')

        self.squeeze()
        sq = self.squeezeLen()
        plt.text(x = 80, y = self.data["Low"].min(), s = "Daily Squeeze = " + str(sq), fontsize = 8, color='b')

        self.squeezeWeekly()
        sq = self.squeezeLenWeekly()
        plt.text(x = 110, y = self.data["Low"].min(), s = "Weekly Squeeze = " + str(sq), fontsize = 8, color='b')

        fig.autofmt_xdate()
        fig.tight_layout()
        figfile = BytesIO()
        fig.savefig(figfile, format='png')
        figfile.seek(0)
        figdata_png = base64.b64encode(figfile.getvalue()).decode('utf-8')
        self.chartURI = 'data:image/png;base64,{}'.format(figdata_png)
        plt.close()

