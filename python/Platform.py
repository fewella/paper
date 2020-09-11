import time
import math

from Core import Core
from Brain import Brain

class Platform:
    # TODO: IMPLEMEMNT A BUY QUEUE -  stocks that I want to buy should be put on a stock . 
    # If the buy queue ("wish list?") is not empty and I'm low on buying power, sell my postition with the highest RSI

    # TODO: 
    
    def __init__(self):
        self.delta = 45
        self.prospective_buy = self.get_prospective()
        
        # Dictionary: symbol->{qty: int, entry_price: float}
        self.positions = {}
        self.original_buying_power = 1000
        self.buying_power = self.original_buying_power

        self.core = Core()
        self.brain = Brain()

        self.overbought = 70.0
        self.oversold   = 30.0


        # do not buy a stock at a higher price than last sold
        # dict: symbol (str) -> last price sold (float)
        self.last_sold = {}

        # do not hold onto a stock for too long - UNLESS: it remains very underbought or is increasing in price quickly
        # for now, just sell off stocks doing well that I've held onto for a while to speed up the algorithm
        # last_bought: dict: symbol (str) -> (dict: "price" -> int, "time" -> int)
        # self.last_bought = {}

        self.wishlist = []


    def run(self):
        '''
        Actually runs the trading algorithm. Loops through potential stocks to buy/sell every delta time.
        The vast majority of algoirthmic thinking should be done in Brain. 
        Platform should only execute these strategies at a very high level.
        '''
        
        self.startup() 

        while True:

            # BUY CYCLE:    
            for symbol in self.prospective_buy:
                
                rsi = self.brain.RSI(symbol)
                print("rsi for " + symbol + ": " + str(rsi))
                
                if rsi < self.oversold:
                    p = self.get_curr_price(symbol)
                    self.buy_portion(symbol, p)


            # SELL CYCLE:
            my_stocks = self.core.get_my_assets()
            for position in my_stocks:
                symbol = position["symbol"]
                rsi = self.brain.RSI(position["symbol"])
                if rsi > self.overbought or len(self.wishlist) > 0 or float(position["unrealized_pl"]) > 0.50:
                    curr_price = position["current_price"]
                    entry_price = position["avg_entry_price"]
                    n = int(position["qty"])
                    
                    if curr_price > entry_price:
                        print("selling: ", symbol)
                        self.sell_all(symbol, n, self.get_curr_price(symbol))
            print("wish list: "  , self.wishlist)
            time.sleep(self.delta)


    def buy_portion(self, symbol, price_per_share):
        # Buys as stock as portion of buying power
        # symbol: str: stock to buy
        # price_per_share: float: 
        # TODO: should have an actual way to find portion. For now, just use 0.25 of original buying power
        # (this means we should only hold onto 4 different stocks at any point in time) 
        
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
            print("Failure. Exiting with code 1...")
            exit(1)

        self.update_buying_power_and_positions()


    def update_buying_power_and_positions(self):
        self.buying_power = self.original_buying_power
        for pos in self.core.get_my_assets():
            self.buying_power -= (float(pos["qty"]) * float(pos["avg_entry_price"]))
            self.positions[pos["symbol"]] = {
                "qty" : pos["qty"],
                "entry_price" : pos["avg_entry_price"]
            }


    def get_curr_price(self, symbol):
        return self.brain.get_data(symbol, "1Min", limit=1)[0]["c"]

        
    def get_prospective(self):
        return [
            'INTC', 
            'AMD', 
            'ATVI', 
            'ZG', 
            'TIVO', 
            'T', 
            'GE', 
            'SNAP', 
            'TWTR', 
            'FIT', 
            'VZ', 
            'CSCO', 
            'OPRA', 
            'IMAX', 
            'HPQ', 
            'XRX', 
            'NTGR', 
            'JNPR', 
            'CHGG', 
            'DELL', 
            'ALRM', 
            'LOGI', 
            'ORCL', 
            'SNE', 
            'BBY',
            'CHK',
            'SPY',
            'BAC',
            'F',
            'T',
            'NIO',
            'VXX',
            'AAL',
            'IDEX',
            'CCL',
            'M',
            'MFA',
            'WFC',
            'DAL',
            'ENPH',
            'VALE',
            'SAVE',
            'NOK',
            'MGM',
            'RCL',
            'CLDR',
            'C',
            'PINS',
            'ROKU'
        ]