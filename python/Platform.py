import time
import math
import threading
import datetime
import asyncio
import logging

from Core import Core
from Brain import Brain

import Util

ORIGINAL_BUYING_POWER = 10000

class Platform:

    class Holding:
        def __init__(self, n, entry):
            self.qty = n
            self.entry_price = entry
        def get_qty(self):
            return self.qty
        def get_entry_price:
            return self.entry_price
        def reset:
            self.qty = 0
            self.entry_price = -1
    
    def __init__(self, c, b, time_period=5):
        self.time_period_minutes = time_period
        self.time_period = None
        if time_period == 1:
            self.time_period = "1Min"
        if time_period == 5:
            self.time_period = "5Min"
        if time_period == 15:
            self.time_period = "15Min"
        if time_period == 1440:
            self.time_period = "1Day"
        #self.time_period_string = self.determine_time_period(self.time_period_minutes)

        self.delta = 60 # seconds to wait between loops TODO this could be related to time_period
        self.prospective_buy = []
        
        self.positions = {} # symbol (str) -> Holding
        self.original_buying_power = ORIGINAL_BUYING_POWER
        self.buying_power = self.original_buying_power

        self.core = c
        self.brain = b

        self.overbought = 70.0
        self.oversold   = 30.0

    
    def should_buy(self, symbol, line=None):
        # TODO EUNICE
        # rsi_line hold a list of rsi values. Should buy should return true if there is a MINIMUM at the END of rsi_line
        
        rsi_line = []
        if line == None:
            rsi_line = Core.dynamic_rsi[symbol]
        else:
            rsi_line = line

        epsilon = 0.5 # tolerance for upward or downward movements
        
        # look at the past 7 values except for the last two:
        curr_line = rsi_line[-10:-3]
        
        for i in range(1, len(curr_line)):
            curr = curr_line[i]
            prev = curr_line[i-1]
            if curr > prev + epsilon:
                # probabily increasing, we dont care
                return False
        if rsi_line[-2] > rsi_line[-3] and rsi_line[-1] > rsi_line[-2]:
            return True
        
        return False


    
    def should_sell(self, symbol, line=None):
        # TODO EUNICE
        # rsi_line hold a list of rsi values. Should buy should return true if there is a MAXIMUM at the END of rsi_line
        rsi_line = Core.dynamic_rsi[symbol]
        return self.should_buy(symbol, line=[-x for x in rsi_line])
    
    
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

        while True:
            for symbol in self.prospective_buy:
                if Core.fresh[symbol]:
                    if self.should_buy(symbol):
                        self.buy_portion(symbol)
                    elif self.should_sell(symbol):
                        self.sell_all(symbol)
            Core.fresh[symbol] = False

            time.sleep(self.delta)
        


    def buy_portion(self, symbol):
        # Buys as stock as portion of buying power
        # symbol: str: stock to buy
        
        portion = 0.20
        price = self.core.get_price(symbol)
        logging.debug("price of", symbol, "is ", price)
        can_buy_exact = self.original_buying_power / price
        n = math.floor(can_buy_exact * portion)

        if n * price <= self.buying_power:
            logging.info("buying " + str(n) + " of " + symbol)
            res = self.core.place_order(symbol, n, "buy", order_type="market")
        
        self.update_buying_power_and_positions()
    

    def sell_all(self, symbol):
        n = self.positions[symbol].qty
        self.core.place_order(symbol, n, side='sell', order_type="limit", time_in_force="gtc")
        # TODO check if successful
        self.positions[symbol].reset()


    def startup(self, time_periods=300):
        logging.info("Testing authorization...")
        if not self.core.test_auth():
            logging.error("Could not authenticate. Exiting with code 1...")
            exit(1)
        else:
            logging.info("Authorization successful")

        # TODO: there are a LOT of magic numbers here - they should be put into globals or class vars.
        # TODO: this whole code block should be moved to Brain
        self.prospective_buy = Util.retrieve_hand_picked_symbols()

        initial_data = self.core.get_data(self.prospective_buy, self.time_period, limit=time_periods)
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
                Core.most_recent_price[symbol] = curr
            
            Core.prev_gain[symbol] = gain
            Core.prev_loss[symbol] = loss
            Core.prev_time[symbol] = prev_time
            Core.prev_close[symbol] = prev_close
            Core.fresh[symbol] = True

        Core.clock_start = time.time()
        self.update_buying_power_and_positions()


    def update_buying_power_and_positions(self):
        self.buying_power = self.original_buying_power
        for pos in self.core.get_positions():
            n = int(pos.qty)
            price = float(pos.avg_entry_price)
            cost = n * price
            self.buying_power -= cost
            self.positions[pos.symbol] = Holding(n, price)

