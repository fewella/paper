import requests
import json

import numpy as np

import Secrets

domain = "https://data.alpaca.markets"

class Brain:
    """
    This class does anything and everything data and algorithm related.
    """

    def __init__(self):
        self.API_KEY = Secrets.API_KEY
        self.SECRET_KEY = Secrets.SECRET_KEY

    
    def __get_auth_header(self):
        return {
            "APCA-API-KEY-ID"     : self.API_KEY, 
            "APCA-API-SECRET-KEY" : self.SECRET_KEY
        }
    
    
    def n_moving_average(self, n, symbol, timeframe="day"):
        """
        Calculates the n-day or n-minute moving average of a stock

        Parameters:
            n: how many days: [1, 1000]
            symbol: which stock
            timeframe: granularity of data: "day" or "minute"

        Returns:
            A dict of the open, high, low, and close moving averages (referenced as "o", "h", "l", and "c"). 
            If unsure, close ("c") is most popular
        """
        
        moving_averages = {
            "o" : 0,
            "h" : 0,
            "l" : 0,
            "c" : 0
        }
        
        bars = self.get_data(symbol, timeframe, limit=n)
        for bar in bars:
            for t in moving_averages:
                moving_averages[t] += bar[t]
        for t in moving_averages:
            moving_averages[t] /= len(bars)
        
        return moving_averages


    def MFI(self, symbol, timeframe="1Min", n=14):
        '''
        Calculate the MFI of a symbol. 
        MFI > 80 : overbought  -> SELL
        MFI < 20 : underbought -> BUY
        Sometimes 90 and 10 are used as thresholds instead. Try with both, maybe add as parameter

        symbol: str symbol
        timeframe: "minute", "1Min", "5Min", "15Min", "day", or "1D". If not provided, defaults to "1Min"
        n: how many time periods to run RSI. If not provided, defaults to 14
        '''
        
        # https://www.investopedia.com/terms/m/mfi.asp

        bars = self.get_data(symbol, timeframe, limit=n+1)
        positive_money_flow = 0
        negative_money_flow = 0
        prior_typical_price = -1
        for bar in bars:
            typical_price = (bar["h"] + bar["l"] + bar["c"]) / 3.0
            raw_money_flow = typical_price * bar["v"]
            if typical_price > prior_typical_price:
                positive_money_flow += raw_money_flow
            else:
                negative_money_flow += raw_money_flow

            prior_typical_price = typical_price

        money_flow_ratio = positive_money_flow/negative_money_flow
        money_flow_index = 100 - (100/(1 + money_flow_ratio))

        print(money_flow_index)

        return money_flow_index

    
    def OBV(self, symbol, timeframe="1Min", n=15):
        '''
        Calculate the On-Balance Volume, giving a symbol, timeframe, and length
        OBV is a momentum trading indicator based on volume. Momentum indicators detect momentum, and indicate whether a position will continue its current trend.
        '''

        obv = 0


        return obv
    
    def RSI(self, symbol, timeframe="1Min", n=15):
        '''
        Calculates the relative stength index of a stock given a timeframe and length
        Returns a float between 0 and 100

        symbol: str symbol to get data
        timeframe: "minute", "1Min", "5Min", "15Min", "day", or "1D". If not provided, defaults to "1Min"
        n: how many time periods to run RSI. If not provided, defaults to 15
        '''
        ups = []
        downs = []
        
        data = self.get_data(symbol, timeframe, limit=n)
        for i in range(1, len(data)):
            today = data[i]['c']
            prev = data[i-1]['c']

            if today > prev:
                ups.append(today - prev)
            elif today < prev:
                downs.append(prev - today)
        
        if len(ups) == 0:
            rs = 0
        elif len(downs) == 0:
            rs = 9999999999999
        else:
            rs = np.array(ups).mean() / np.array(downs).mean()
        rsi = 100 - 100 / (1 + rs)

        return rsi
    
    def get_data(self, symbol, timeframe, limit=0, start=None, end=None):
        '''
        Uses the bars method from ,
        Returns an array of dictionaries, where each dictionary contains the open ('o'), close ('c'), high ('h'), low ('l'), and volume ('v')

        symbol: str symbol to get data
        timeframe: "minute", "1Min", "5Min", "15Min", "day", or "1D"
        limit: max number of bars to return 
        start: data must come at or after timestamp start
        end: data must come at or before timestamp end
        '''
        method = "/v1/bars/" + timeframe

        method += ("?symbols=" + symbol)
        method += ("&limit=" + str(limit))

        if start != None:
            method += ("&start=" + start)

        if end != None:
            method += ("&end=" + end)
        
        r = requests.get(domain + method, headers=self.__get_auth_header())
        code = r.status_code
        if code == 200:
            return list(json.loads(r.text)[symbol])
        else:
            print("Get data failed with error code " + str(code))
            print(r.text)
            return []
    