import time
import math
import threading
import datetime
import asyncio
import logging

import Core
import Brain
import Util

import matplotlib.pyplot as plt
import datetime

ORIGINAL_BUYING_POWER = 10000


def run():
    pass


def display_graph(self, symbol, text="", debug=False):
    rsi_to_display = Core.dynamic_rsi[symbol][-10:]
    price_to_display = Core.historic_price[symbol][-10:]

    timestamps = []
    ticks = []
    now = datetime.datetime.now()
    for i in range(10):
        curr = now - datetime.timedelta(seconds=i)
        timestamps.append(curr.strftime("%H:%M:%S"))
        ticks.append(i)
    timestamps = timestamps[::-1]
    
    fig, ax = plt.subplots()
    plt.xticks(ticks, timestamps, rotation=45)
    
    color1 = "tab:red"
    color2 = "tab:blue"
    
    plot1 = ax.plot(rsi_to_display, label="RSI", color=color1)
    ax.set_ylabel("RSI", color=color1)
    ax.tick_params(axis='y', labelcolor=color1)
    
    ax2 = ax.twinx()
    plot2 = ax2.plot(price_to_display, label="Price", color=color2)
    ax2.set_ylabel('Price', color=color2)
    ax2.tick_params(axis='y', labelcolor=color2)
    
    plots = plot1 + plot2
    labels = [plot.get_label() for plot in plots]
    plt.legend(plots, labels, loc='upper right', framealpha=0.7)
    plt.annotate(text, (7, price_to_display[7]), xytext=(7.2, price_to_display[7] + 1))
    plt.scatter(7, price_to_display[7], color='black', zorder=10)
    plt.title("Stock: ", symbol)

    plt.show()
