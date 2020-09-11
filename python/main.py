from sys import argv

from Core import Core
from Brain import Brain
from Platform import Platform

def custom():
    core = Core()
    core.place_order("TWTR", 6, side="sell", order_type="market")

if __name__ == "__main__":
    
    argc = len(argv)
    if argc > 2:
        print("Usage: python main.py [behavior]")
    
    if argc == 2 and argv[1] == "--custom":
        custom()
    else:
        platform = Platform()
        platform.run()
    