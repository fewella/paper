import urllib.request

def retrieve_all_symbols():
    '''
    Gets current list of stock symbols traded on the market, and returns them as a list of strings
    Currently, just grabs NYSE. Future versions should allow choice of which exchange(s)
    Future versions should also include some extra data on the symbols
    '''

    nyse_symbol_url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt"
    return [line.split("|")[0] for line in urllib.request.urlopen(nyse_symbol_url).read().decode().split('\r\n')][1:-2]


def get_channels():
	pass


def retrieve_hand_picked_symbols():
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
