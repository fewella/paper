from sys import stderr

import Core
import Brain
import Platform
import Parameters

import Util

import logging
import argparse


def custom():
    ''' Invoke with -c, --custom '''
    
    print(Core.get_data(["AAPL", "GOOG"], "day", limit=20))

    rsi = Brain.RSI("ROKU", timeframe="15Min")
    print(rsi)


if __name__ == "__main__":
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

    bar_duration = 1 # Default - use minute bars
    if args.timeframe:
        try:
            bar_duration = int(args.timeframe)
        except:
            logging.critical("Please enter an integer for minutes. Exiting....")
            exit()
        if bar_duration < 1 or bar_duration > 1440:
            logging.critical("Please enter a number of minutes between 1 and 1440. Exiting....")
            exit()


    Parameters.init(bar_duration)
    Platform.run()

