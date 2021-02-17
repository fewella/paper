import time
import math
import threading
import datetime
import asyncio
import logging

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
    
    
    def thread_target(self):
        asyncio.run(self.core.init_stream())
    
    
    def should_buy(self, symbol):
        # TODO EUNICE
        # rsi_line hold a list of rsi values. Should buy should return true if there is a MINIMUM at the END of rsi_line
        rsi_line = Core.dynmaic_rsi[symbol]


    
    def should_sell(self, symbol):
        # TODO EUNICE
        # rsi_line hold a list of rsi values. Should buy should return true if there is a MAXIMUM at the END of rsi_line
        # [66, 73, 74, 74.5, 76, 70, 64]
        rsi_line = Core.dynmaic_rsi[symbol]
    
    
    def run(self):
        '''
        Actually runs the trading algorithm. Loops through potential stocks to buy/sell every delta time.
        The vast majority of algoirthmic thinking should be done in Brain. 
        Platform should only execute these strategies at a very high level.
        '''
        
        self.startup() 

        t = threading.Thread(target=self.core.init_stream)
        t.start()
        
        logging.info("WebSockets live")
        


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
        
        self.update_buying_power_and_positions()
    

    def sell_all(self, symbol, n, curr_price):
        self.core.place_order(symbol, n, side='sell', order_type="limit", time_in_force="gtc", limit_price=curr_price)


    def startup(self):
        logging.info("Testing authorization...")
        if not self.core.test_auth():
            logging.error("Could not authenticate. Exiting with code 1...")
            exit(1)
        else:
            logging.info("Authorization successful")

        # TODO: there are a LOT of magic numbers here - they should be put into globals or class vars.
        # This whole code block should be moved to Brain
        self.prospective_buy = Util.retrieve_hand_picked_symbols()

        # TODO (AJAY) Make limit a parameter of the function
        initial_data = self.core.get_data(self.prospective_buy, "15Min", limit=300)
        for symbol in initial_data:
            Core.dynamic_rsi[symbol] = []

            bars = initial_data[symbol]
            # Calculate the first RSI
            gain = 0
            loss = 0
            for i in range(1, 14):
                curr = bars[i].c
                prev = bars[i-1].c
                change = curr - prev
                if change > 0:
                    gain += change
                else:
                    loss -= change
            gain /= 14
            loss /= 14
            if loss == 0:
                rs = 1
            else:
                rs = gain/loss
            rsi = 100 - 100 / (1 + rs)

            # Then calculate continued RSIs
            prev_close = -1
            prev_time = -1
            for i in range(15, len(bars)):
                curr = bars[i].c
                prev = bars[i-1].c
                change = curr - prev
                if change > 0:
                    gain = (gain * 13 + change) / 14
                    loss = loss * 13/14
                else:
                    gain = gain * 13/14
                    loss = (loss * 13 - change) / 14
                rs = gain/loss
                rsi = 100 - 100 / (1 + rs)
                prev_close = curr
                prev_time = bars[i].t.value / 10**9
                Core.dynamic_rsi[symbol].append(rsi)
            
            Core.prev_gain[symbol] = gain
            Core.prev_loss[symbol] = loss
            Core.prev_time[symbol] = prev_time
            Core.prev_close[symbol] = prev_close

        Core.clock_start = time.time()
        self.update_buying_power_and_positions()


    def update_buying_power_and_positions(self):
        self.buying_power = self.original_buying_power
        for pos in self.core.get_positions():
            self.buying_power -= (float(pos.qty) * float(pos.avg_entry_price))
            self.positions[pos.symbol] = {
                "qty" : pos.qty,
                "entry_price" : pos.avg_entry_price
            }

