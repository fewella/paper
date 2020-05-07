import time
import math

from Core import Core
from Brain import Brain

class Platform:
    
    
    def __init__(self):
        self.delta = 60
        self.prospective_buy = self.get_prospective()
        
        # Dictionary: symbol->{qty: int, entry_price: float}
        self.holdings = {}
        self.original_buying_power = 500
        self.buying_power = self.original_buying_power

        self.core = Core()
        self.brain = Brain()


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
                # Current algorithm: if moving average for past 5 mins is greater than past 20 mins, buy
                MA_5mins  = self.brain.n_moving_average( 5, symbol, "minute")["c"]
                MA_20mins = self.brain.n_moving_average(20, symbol, "minute")["c"]

                if MA_5mins > MA_20mins:
                    self.buy_portion(symbol, MA_5mins)
                
                self.startup()


            # SELL CYCLE:
            stocks = self.core.get_my_assets()
            for stock in stocks:
                print("symbol: " + str(stock["symbol"]))
                print("qty: " + str(stock["qty"]))

                symbol = stock["symbol"]
                price = float(stock["market_value"])
                entry_price = float(stock["avg_entry_price"])

                MA_5mins  = self.brain.n_moving_average( 5, symbol, "minute")["c"]
                MA_20mins = self.brain.n_moving_average(20, symbol, "minute")["c"]

                if MA_5mins < MA_20mins and price > entry_price:
                    self.sell_all(symbol, float(stock["qty"]), price)
                
                self.update_buying_power()
            

            
    def buy_portion(self, symbol, price_per_share):
        # Buys as stock as portion of buying power
        # symbol: str: stock to buy
        # price_per_share: float: 
        # TODO: should have an actual way to find portion. For now, just use 0.25 of original buying power
        # (this means we should only hold onto 4 different stocks at any point in time) 
        
        portion = 0.25
        can_buy_exact = self.original_buying_power / price_per_share
        n = math.floor(can_buy_exact * portion)

        res = self.core.place_order(symbol, n, "buy", order_type="market")
    

    def sell_all(self, symbol, n, curr_price):
        self.core.place_order(symbol, n, side='sell', order_type="limit", time_in_force="gtc", limit_price=curr_price)


    def startup(self):
        print("Testing auth...")
        if not self.core.test_auth():
            print("Failure. Exiting with code 1...")
            exit(1)
        
        self.update_buying_power()
    
    def update_buying_power(self):
        self.buying_power = self.original_buying_power
        for pos in self.core.get_my_assets():
            self.buying_power -= (float(pos["qty"]) * float(pos["avg_entry_price"]))
        
        
        
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
            'BBY'
        ]