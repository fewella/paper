import requests
import json

domain = "https://data.alpaca.markets"

class Brain:
    """
    This class does anything and everything data and algorithm related.
    """

    def __init__(self):
        self.API_KEY = "PKBZJXADC72D0Z9B1TME"
        self.SECRET_KEY = "2YPuW7wK5UOLZwx3/Nn1NQXWVrjyNhNLVvCh5i87"
    
    
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
        
        bars = self.get_data(timeframe, symbol, limit=n)
        for bar in bars:
            for t in moving_averages:
                moving_averages[t] += bar[t]
        for t in moving_averages:
            moving_averages[t] /= len(bars)
        
        return moving_averages



    def get_data(self, timeframe, symbol, limit=0, start=None, end=None):
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
