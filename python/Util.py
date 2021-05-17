import traceback
import logging
import urllib.request

import yfinance as yf
import numpy as np

def retrieve_all_symbols():
    '''
    Gets current list of stock symbols traded on the market, and returns them as a list of strings
    Currently, just grabs NYSE. Future versions should allow choice of which exchange(s)
    Future versions should also include some extra data on the symbols
    '''

    nyse_symbol_url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt"
    return [line.split("|")[0] for line in urllib.request.urlopen(nyse_symbol_url).read().decode().split('\r\n')][1:-2]


def retrieve_active_symbols(n=300, force_fetch=False):
    '''
    Retrieve the n most traded symbols over the past month
    force_fetch: force a pull from yfinance of most traded stocks, even if set of symbols already downloaded. This will take a while.
    '''

    symbols_filename = "actively_traded_symbols.txt"
    active_symbols = []
    downloaded = True
    try:
        f = open(symbols_filename, "r")
        for line in f:
            active_symbols.append(line.rstrip("\n"))
        f.close()
    except FileNotFoundError as e:
        downloaded = False
    except Exception as e:
        logging.error("Unknown error retrieving symbols")
        traceback.print_exc()
        exit(-1)
    
    if (not downloaded) or force_fetch:
        all_symbols = retrieve_all_symbols()
        volume = {}
        for s in all_symbols:
            try:
                ticker = yf.Ticker(s)
                data = ticker.history(period="1mo")
                volume[s] = np.mean(data["Volume"])
                print("volume of " + s + " is " + str(volume[s]))
            except:
                print(":)?")
                traceback.print_exc()
                continue

        volume = dict(sorted(volume.items(), key=lambda x : x[1]))
        i = 0
        for symbol in volume:
            active_symbols.append(symbol)
            i += 1
            if i == n:
                break
        
        f = open(symbols_filename, "w")
        for s in active_symbols:
            f.write(s + "\n")
        f.close()
    
    return active_symbols
