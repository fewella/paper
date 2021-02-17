import json
import time
import asyncio
import logging
import requests
import websockets

import Util

import alpaca_trade_api as tradeapi

ACCOUNT_STATUS_ACTIVE = "ACTIVE"

#core_domain = "https://api.alpaca.markets"
core_domain = "https://paper-api.alpaca.markets"
data_domain = "https://data.alpaca.markets"

conn = tradeapi.StreamConn(data_stream='polygon', base_url='wss://data.alpaca.markets')


@conn.on(r'^AM.*')
async def on_minute_bars(conn, channel, bar):
    # TODO (Ajay) - update Core.dynamic_rsi with relevant information.
    symbol = bar.symbol
    epsilon = 30
    bar_time = bar.end.value / 10**9
    time_range_floor = (60 * 15 - epsilon) + Core.prev_time[symbol]
    time_range_ceil  = (60 * 15 + epsilon) + Core.prev_time[symbol]
    if time_range_floor < bar_time and bar_time < time_range_ceil:
        curr = bar.close
        change = curr - Core.prev_close[symbol]
        if change > 0:
            Core.prev_gain[symbol] = (Core.prev_gain[symbol] * 13 + change) / 14
            Core.prev_loss[symbol] *= (13/14)
        else:
            Core.prev_gain[symbol] *= (13/14)
            Core.prev_loss[symbol] = (Core.prev_loss[symbol] * 13 - change) / 14
        
        rs  = Core.prev_gain[symbol] / Core.prev_loss[symbol]
        rsi = 100 - 100 / (1 + rs)
        Core.prev_close[symbol] = curr
        
        Core.dynamic_rsi[symbol].append(rsi)
        print("added to dynmic rsi for ", symbol, "! recent list: ", Core.dynamic_rsi[symbol][-10:])
    else:
        print("Not correct time interval, do nothing :)")

    
class Core:
    '''
    Responsible for all API calls. Orders and all communication should be executed via Core. 
    '''

    # time when startup() completes, from epoch in seconds
    
    # dict: symbol (str) -> list of 16 dictionaries represnting the 16 most recent rsi's.
    # on minute bars (on_minute_bars() should implement this), this should be updated - last item removed, and incoming  appeneded. 
    dynamic_rsi = {}
    
    prev_gain = {} # symbol (str) -> previous gain (float), for rsi
    prev_loss = {} # symbol (str) -> previous loss (float), for rsi
    prev_close = {} # symbol (str) -> previous close (float), for rsi
    prev_time = {} # symbol (str) -> last time recorded (int), for bookkeeping


    def __init__(self):
        self.api = tradeapi.REST(base_url=core_domain)
        self.data_api = tradeapi.REST(base_url=data_domain)


    def init_stream(self):
        logging.info("Initializing data streaming via WebSockets...")
        channels = ['trade_updates'] + Util.get_channels()
        try:
            conn.run(channels)
        except Exception as e:
            print("conn.run() error - restarting")
            print(e)
            time.sleep(3)
            self.init_stream(channels)
        

    def test_auth(self):
        account = self.api.get_account()
        return account.status == ACCOUNT_STATUS_ACTIVE


    def get_orders(self):
        return self.api.list_orders()


    def place_order(self, symbol, n, side="sell", order_type="market", time_in_force="day", limit_price=None, stop_price=None, extended_hours=False):
        '''
        Places an order on the market. 
        Requires symbol (str), n (int)
        
        Optional parameters:
        
        side: "sell" or "buy" (default "sell")
        
        order_type: "market", "limit", "stop", or "stop_limit" (default "market") 
            "limit" requires limit_price, "stop" requires stop_price, "stop_limit" requries both
        
        limit_price: int, > 0: 
        '''

        self.api.submit_order(symbol, n, side, order_type, time_in_force, limit_price=limit_price, stop_price=stop_price)
    
    
    def cancel_order(self, order_id):
        self.api.cancel_order(order_id)


    def cancel_all_orders(self):
        self.api.cancel_all_orders()
        

    def get_positions(self):
        '''
        Returns a list of dictionaries, each containing attributes like "symbol", "avg_entry_price", "qty", "current_price", and many more
        list of all attributes at https://alpaca.markets/docs/api-documentation/api-v2/positions/

        return list if successful, empty list if failed
        '''

        return self.api.list_positions()
    
    
    def get_available_assets(self):
        return self.api.list_assets()
    
    
    def get_data(self, symbol, timeframe, limit=0, start=None, end=None, after=None, until=None):
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
        data = self.data_api.get_barset(symbol, timeframe, limit, start=start, end=end, after=after, until=until)

        if type(symbol) == str:
            return dict(data)[symbol]
        else:
            return dict(data)
    

    def get_high_volume_symbols(self, initial_list):
        # TODO (eventually) technically determine good symbols to trade. Currently hardcoded list in Util. 
        pass


    def test_asset(self, symbol):
        self.api.get_asset(symbol)

