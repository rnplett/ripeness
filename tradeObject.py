import pandas as pd
import quandl
import json
import sys
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

    def daGoogleCSV(self,sym='SPY',start='Jan+1,+2008', end=None):
        try:
            p = pd.read_csv('https://finance.google.com/finance/historical?q=' + sym + '&startdate=' + start + '&output=csv')
        except:
            try:
                p = pd.read_csv('https://finance.google.com/finance/historical?q=NYSE:' + sym + '&startdate=' + start + '&output=csv')
            except:
                print(sym + " - Google lookup error")

        p = p[::-1]
        p = p.reset_index(drop=True)
        self.data = p

    def daQuandl(self,sym='SPY'):
        try:
            p = pd.read_csv('https://www.quandl.com/api/v3/datasets/WIKI/' + sym + '/data.csv?api_key=' + QUANDL_API_KEY)
        except:
            print(sym + " - Quandl lookup error")

        p = p[::-1]
        p = p.reset_index(drop=True)
        self.data = p
