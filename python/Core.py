import requests
import json

import asyncio
import websockets
import alpaca_trade_api as tradeapi

import Secrets

# TODO: put URLS and other constants in another file
ACCOUNT_STATUS_ACTIVE = "ACTIVE"

#core_domain = "https://api.alpaca.markets"
core_domain = "https://paper-api.alpaca.markets"
data_domain = "https://data.alpaca.markets"

conn = tradeapi.StreamConn(data_stream='polygon', base_url='wss://data.alpaca.markets')

@conn.on(r'^AM$')
async def on_minute_bars(conn, channel, bar):
    print('bars', bar)


@conn.on(r'^A$')
async def on_second_bars(conn, channel, bar):
    print('bars', bar)

class Core:
    '''
    Responsible for all API calls. Orders and all communication should be executed via Core. 
    TODO: make all manual web requests through alpaca_trade_api
    '''

    def __init__(self):
        self.API_KEY = Secrets.API_KEY
        self.SECRET_KEY = Secrets.SECRET_KEY

        self.api = tradeapi.REST(base_url=core_domain)
        self.data_api = tradeapi.REST(base_url=data_domain)


    def __get_auth_header(self):
        return {
            "APCA-API-KEY-ID"     : self.API_KEY,
            "APCA-API-SECRET-KEY" : self.SECRET_KEY
        }


    async def init_stream(self):
        await conn.run(['trade_updates', 'AM.*', 'A.TSLA'])
        

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
        self.cancel_order(order_id)


    def cancel_all_orders(self):
        self.cancer_all_orders()
        

    def get_positions(self):
        '''
        Returns a list of dictionaries, each containing attributes like "symbol", "avg_entry_price", "qty", "current_price", and many more
        list of all attributes at https://alpaca.markets/docs/api-documentation/api-v2/positions/

        return list if successful, empty list if failed
        '''

        return self.api.list_positions()
    
    
    def get_available_assets(self):
        '''
        Returns a list of tradable assests
        TODO: Maybe use instead of nyse stock thing in Util.py
        '''

        return self.api.list_assets()
    
    
    def get_data(self, symbol, timeframe, limit=0, start=None, end=None, after=None, until=None):
        '''
        Uses the bars method from ,
        Returns an array of dictionaries, where each dictionary contains the open ('o'), close ('c'), high ('h'), low ('l'), and volume ('v')

        symbol: str symbol to get data
        timeframe: "minute", "1Min", "5Min", "15Min", "day", or "1D"
        limit: max number of bars to return 
        start: data must come at or after timestamp start (after: data must comes AFTER timestamp after)
        end: data must come at or before timestamp end (until: data must come BEFORE timestamp until)
        '''
        data = self.data_api.get_barset(symbol, timeframe, limit, start=start, end=end, after=after, until=until)

        # TODO: make this work for multiple symbols. Generally we want to make fewer requests.
        # but only we should only be using this at setup and streaming the rest of the data. big monkahmm. 
        return dict(data)[symbol]

    def test_asset(self, symbol):
        # TODO: figure out what this actually does
        self.api.get_asset(symbol)

