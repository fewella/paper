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
'''


def custom():
    ''' This is strictly for testing, invoke with -c, --custom'''
    
    c = Core()
    b = Brain(c)

    print(c.get_data("AAPL", "day", limit=20))
    
    rsi = b.RSI("ROKU", timeframe="15Min")
    print(rsi)


if __name__ == "__main__":

    nest_asyncio.apply()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--custom", help="run the custom function and exit - for testing",
                                    action="store_true")
    parser.add_argument("-d", "--debug", help="log debug messages",
                                    action="store_true")
    parser.add_argument("-q", "--quiet", help="suppresses all output except critical, overrides debug",
                                    action="store_true")
    parser.add_argument("-o", "--output", help="store all output in the specified file")
    parser.add_argument("-t", "--timeframe", help="specify the timeframe over which to calculate signals and make trades, in MINUTES - [1, 1440]")
    args = parser.parse_args()

    if args.custom:
        custom()
        exit()
    
    l = logging.INFO
    if args.debug:
        l = logging.DEBUG
    if args.quiet:
        l = logging.CRITICAL

    if args.output:
        logging.basicConfig(filename=args.output, level=l)
    else: 
        logging.basicConfig(stream=stderr, level=l)


    core = Core()
    brain = Brain(core)
    
    platform = Platform(core, brain)
    platform.run()
    
