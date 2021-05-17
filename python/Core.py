import json
import time
import asyncio
import logging
import requests
import websockets
import traceback

import Util

NANOSEC = 10**9

'''
Responsible for all API calls. Orders and all communication should be executed via Core. 
'''

dynamic_rsi = {}

prev_gain = {} # symbol (str) -> previous gain (float), for rsi
prev_loss = {} # symbol (str) -> previous loss (float), for rsi
prev_close = {} # symbol (str) -> previous close (float), for rsi
prev_time = {} # symbol (str) -> last time recorded (int), for bookkeeping

fresh = {} # symbol (str) -> bool: whether new data is available for analysis

most_recent_price = {} # symbol(str) -> float, most recent price of the given asset
historic_price = {} # symbol (str) -> list[float], most recent 


def test_auth():
    pass


def get_price(symbol):
    pass


def get_orders(self):
    pass


def place_order(self, symbol, n, side, order_type="market", time_in_force="day", limit_price=None, stop_price=None, extended_hours=False):
    '''
    Places an order on the market. 
    Requires symbol (str), n (int)
    
    Optional parameters:
    
    side: "sell" or "buy" (default "sell")
    
    order_type: "market", "limit", "stop", or "stop_limit" (default "market") 
        "limit" requires limit_price, "stop" requires stop_price, "stop_limit" requries both
    
    limit_price: int, > 0: 
    '''

    pass
    

def get_positions(self):
    '''
    Returns a list of dictionaries

    return list if successful, empty list if failed
    '''

    return {}


def get_data(symbol, timeframe, limit=0, start=None, end=None, after=None, until=None):
    '''
    Returns an array of dictionaries, where each dictionary contains the open ('o'), close ('c'), high ('h'), low ('l'), and volume ('v')
    If symbol is a list, the described dictionaries are indexible 
    EG: get_data(["AAPL", "GOOG"], "day")["AAPL"]
    

    symbol: str or list[str] of symbol(s) to get data
    timeframe: "minute", "1Min", "5Min", "15Min", "day", or "1D"
    limit: max number of bars to return
    start: data must come at or after timestamp start (after: data must comes AFTER timestamp after)
    end: data must come at or before timestamp end (until: data must come BEFORE timestamp until)
    '''
    return {}

