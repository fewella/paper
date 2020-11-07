import urllib.request

def retrieve_symbols():
    '''
    Gets current list of stock symbols traded on the market, and returns them as a list of strings
    Currently, just grabs NYSE. Future versions should allow choice of which exchange(s)
    Future versions should also include some extra data on the symbols
    '''

    nyse_symbol_url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt"
    return [line.split("|")[0] for line in urllib.request.urlopen(nyse_symbol_url).read().decode().split('\r\n')][:-2]
