from sys import argv, stderr

from Core import Core
from Brain import Brain
from Platform import Platform

import Util

import logging
import asyncio
import nest_asyncio

'''
Driver B)
No argument run will run the platform and simulation with all defaults.

TODO list:
    -> could add parameters for time period over which signals are calculated
    -> give preference to certain symbols
    -> etc...
'''


def custom():
    ''' This is strictly for testing'''
    
    c = Core()
    b = Brain(c)

    print(c.get_data("AAPL", "day", limit=20))

    rsi = b.RSI("ROKU", timeframe="15Min")
    print(rsi)

    #mfi = b.MFI("AAPL", timeframe="1D")
    #print("mfi:", mfi)

    #macd = b.MACD("GOOG", timeframe="1D")
    #print("macd:", macd)

    #mov = b.n_moving_average(50, "AAPL", timeframe="day")
    #print("50 day mov avg: ", mov)

    #c.place_order("GOOG", 5, side='buy')
    #c.get_orders()

    #asyncio.run(c.init_stream())


if __name__ == "__main__":

    nest_asyncio.apply()
    logging.basicConfig(stream=stderr, level=logging.DEBUG)
    
    argc = len(argv)
    if argc > 2:
        print("Usage: python main.py [behavior]")
    
    if argc == 2:
        if argv[1] == "--custom":
            custom()
            
    else:
        core = Core()
        brain = Brain(core)
        
        platform = Platform(core, brain)
        platform.run()
    