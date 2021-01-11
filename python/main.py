from sys import argv

from Core import Core
from Brain import Brain
from Platform import Platform

import Util

import asyncio

'''
Driver B)
No argument run will run the platform and simulation with all defaults.

TODO list:
    -> could add parameters for time period over which signals are calculated
    -> give preference to certain symbols
    -> etc...
'''


def custom():
    c = Core()
    b = Brain(c)
    mfi = b.MFI("AAPL", timeframe="1D")
    print("mfi:", mfi)

    macd = b.MACD("GOOG", timeframe="1D")
    print("macd:", macd)

    #asyncio.run(c.initialize_stream())


if __name__ == "__main__":
    
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
    