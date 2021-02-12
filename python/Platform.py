import time
import math
import threading
import datetime

from Core import Core
from Brain import Brain

import Util

ORIGINAL_BUYING_POWER = 1000

class Platform:
    
    def __init__(self, c, b):
        self.delta = 45 # seconds to wait between loops
        self.prospective_buy = []
        
        # Dictionary: symbol->{qty: int, entry_price: float}
        self.positions = {}
        self.original_buying_power = ORIGINAL_BUYING_POWER
        self.buying_power = self.original_buying_power

        self.core = c
        self.brain = b

        self.overbought = 70.0
        self.oversold   = 30.0

        # do not hold onto a stock for too long - UNLESS: it remains very underbought or is increasing in price quickly
        # for now, just sell off stocks doing well that I've held onto for a while to speed up the algorithm
        # last_bought: dict: symbol (str) -> (dict: "price" -> int, "time" -> int)
        # self.last_bought = {}
    
    
    def run(self):
        '''
        Actually runs the trading algorithm. Loops through potential stocks to buy/sell every delta time.
        The vast majority of algoirthmic thinking should be done in Brain. 
        Platform should only execute these strategies at a very high level.
        '''
        
        self.startup() 

        # TODO Run this in its own thread - don't need to worry about returns or joining the thread. it just needs to run. 
        # in the future we should join it in case it throws an exception, then relaunch. that's an endgame feature though. 
        # asyncio.run(c.init_stream())

        


    def buy_portion(self, symbol, price_per_share):
        # Buys as stock as portion of buying power
        # symbol: str: stock to buy
        # price_per_share: float: price per share lol
        
        portion = 0.20
        can_buy_exact = self.original_buying_power / price_per_share
        print(can_buy_exact)
        n = math.floor(can_buy_exact * portion)

        if n * price_per_share <= self.buying_power:
            print("buying " + str(n) + " of " + symbol)
            res = self.core.place_order(symbol, n, "buy", order_type="market")
        else:
            if symbol not in self.wishlist:
                self.wishlist.append(symbol)
        
        self.update_buying_power_and_positions()
    

    def sell_all(self, symbol, n, curr_price):
        if symbol in self.wishlist:
            self.wishlist.remove(symbol)
        self.core.place_order(symbol, n, side='sell', order_type="limit", time_in_force="gtc", limit_price=curr_price)


    def startup(self):
        print("Testing auth...")
        if not self.core.test_auth():
            print("Could not authenticate. Exiting with code 1...")
            exit(1)
        else:
            print("Auth success!")

        # TODO: there are a LOT of magic numbers here - they should be put into globals or class vars.
        # This whole code block should be moved to Brain
        self.prospective_buy = Util.retrieve_hand_picked_symbols()

        initial_data = self.core.get_data(self.prospective_buy, "15Min", limit=250)
        for symbol in initial_data:
            Core.dynamic_rsi[symbol] = []

            bars = initial_data[symbol]
            for i in range(0, 250-14):
                
                gain = 0
                loss = 0
                for j in range(1, 14):
                    curr = bars[j+i].c
                    prev = bars[j+i-1].c
                    if curr > prev:
                        gain += (curr - prev)
                    else:
                        loss += (prev - curr)
                gain /= 14
                loss /= 14
                rsi = 100 - 100 / (1 + gain/loss)
                Core.dynamic_rsi[symbol].append(rsi)
                

        self.update_buying_power_and_positions()


    def update_buying_power_and_positions(self):
        self.buying_power = self.original_buying_power
        for pos in self.core.get_positions():
            self.buying_power -= (float(pos.qty) * float(pos.avg_entry_price))
            self.positions[pos.symbol] = {
                "qty" : pos.qty,
                "entry_price" : pos.avg_entry_price
            }

