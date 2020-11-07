from sys import argv

from Core import Core
from Brain import Brain
from Platform import Platform

import Util

def custom():
    b = Brain()
    b.MFI("GOOG", timeframe="1D")

if __name__ == "__main__":
    
    argc = len(argv)
    if argc > 2:
        print("Usage: python main.py [behavior]")
    
    if argc == 2:
        if argv[1] == "--custom":
            custom()
    else:
        platform = Platform()
        platform.run()
    