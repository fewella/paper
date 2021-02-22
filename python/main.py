from sys import stderr

from Core import Core
from Brain import Brain
from Platform import Platform

import Util

import logging
import asyncio
import argparse
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


if __name__ == "__main__":

    nest_asyncio.apply()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--custom", help="run the custom function, and exit - for testing",
                                    action="store_true")
    parser.add_argument("-o", "--output", help="store all output in the specified file")
    args = parser.parse_args()

    if args.custom:
        custom()
        exit()
    
    if args.output:
        logging.basicConfig(filename=args.output, level=logging.INFO)
    else: 
        logging.basicConfig(stream=stderr, level=logging.INFO)


    core = Core()
    brain = Brain(core)
    
    platform = Platform(core, brain)
    platform.run()
    
