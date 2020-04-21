import time

from Core import Core
from Brain import Brain

class Platform:
    
    def __init__(self):
        self.delta = 1

    def run(self):
        '''
        Actually runs the trading algorithm. Loops through potential stocks to buy/sell every delta time
        '''

        core = Core()

        print("Testing auth...")
        if not core.test_auth():
            print("Failure. Exiting with code 1...")
            exit(1)

        while True:
            stocks = core.get_assets()

            for stock in stocks:
                print("symbol: " + str(stock["symbol"]))
                print("qty: " + str(stock["qty"]))
                print()

            time.sleep(self.delta)