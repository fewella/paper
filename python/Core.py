import requests
import json

import Secrets

core_domain = "https://paper-api.alpaca.markets"
data_domain = "https://data.alpaca.markets"

class Core:
    '''
    Responsible for all API calls. Orders and all communication should be executed via Core. 
    '''

    def __init__(self):
        self.API_KEY = Secrets.API_KEY
        self.SECRET_KEY = Secrets.SECRET_KEY


    def __get_auth_header(self):
        return {
            "APCA-API-KEY-ID"     : self.API_KEY, 
            "APCA-API-SECRET-KEY" : self.SECRET_KEY
        }
        

    def test_auth(self):
        method = "/v2/account"

        r = requests.get(domain + method, headers=self.__get_auth_header())
        code = r.status_code
        if code == 200:
            print("Authentication success")
            return True
        else:
            print("Authentication failure. Response code: " + str(code))
            print(r.text)
            return False


    def get_orders(self):
        method = "/v2/orders"

        r = requests.get(core_domain + method, headers=self.__get_auth_header())
        print(r.text)


    def place_order(self, symbol, n, side="sell", order_type="market", time_in_force="day", limit_price=-1, stop_price=-1, extended_hours=False):
        '''
        Places an order on the market. 
        Requires symbol (str), n (int)
        
        Optional parameters:
        
        side: "sell" or "buy" (default "sell")
        
        order_type: "market", "limit", "stop", or "stop_limit" (default "market") 
            "limit" requires limit_price, "stop" requires stop_price, "stop_limit" requries both
        
        limit_price: int, > 0: 
        '''
        method = "/v2/orders"

        if n <= 0:
            print("Please provide a valid quantity")
            return False

        if (order_type == "limit" or order_type == "stop_limit") and limit_price == -1:
            print("Please provide a limit price for limit and stop_limit orders")
            return False
        
        if (order_type == "stop" or order_type == "stop_limit") and stop_price == -1:
            print("Please provide a stop price for stop and stop_limit orders ")
            return False
        
        data = {
            "symbol"        : symbol,
            "qty"           : n,
            "side"          : side,
            "type"          : order_type,
            "time_in_force" : time_in_force,
        }

        if limit_price > 0:
            data["limit_price"] = limit_price
        
        if stop_price > 0:
            data["stop_price"] = stop_price

        data = json.dumps(data)

        r = requests.post(core_domain + method, headers=self.__get_auth_header(), data=data)
        code = r.status_code
        if code == 200:
            print("Order placed successfully")
            response_dict = json.loads(r.text)
            return True
        else:
            print("Post request failed with status code " + str(code))
            print(r.text)
            return False
    
    
    def cancel_order(self, order_id):
        method = "v2/orders/" + order_id

        r = requests.delete(core_domain + method, headers=self.__get_auth_header())
        code = r.status_code
        if code == 200:
            print("order cancelled successfully")
            return True
        else:
            print("Request failed with code: " + str(code))
            print(r.text)
            return False


    def cancel_all_orders(self):
        method = "/v2/orders"

        r = requests.delete(core_domain + method, headers=self.__get_auth_header())
        code = r.status_code
        if code == 200:
            print("ALL ORDERS cancelled successfully")
            return True
        else:
            print("Request failed with code: " + str(code))
            print(r.text)
            return False
        

    def get_my_assets(self):
        '''
        Returns a list of dictionaries, each containing attributes like "symbol", "avg_entry_price", "qty", "current_price", and many more
        list of all attributes at https://alpaca.markets/docs/api-documentation/api-v2/positions/
        '''

        method = "/v2/positions"

        r = requests.get(core_domain + method, headers=self.__get_auth_header())
        code = r.status_code
        if code == 200:
            print("get_my_assets() retrieval successful")
            data = json.loads(r.text)
            return list(data)
        else:
            print("Retrieval failed with code: " + str(code))
            print(r.text)
            return []
    
    
    def get_assets(self):
        method = "/v2/assets"

        r = requests.get(core_domain + method, headers=self.__get_auth_header())
        code = r.status_code
        if code == 200:
            print("Get assets successful")
            data = json.loads(r.text)
            return list(data)
        else:
            print("Get assets failed with code: " + str(code))
            print(r.text)
            return []
    
    
    def get_data(self, symbol, timeframe, limit=0, start=None, end=None):
        '''
        Uses the bars method from ,
        Returns an array of dictionaries, where each dictionary contains the open ('o'), close ('c'), high ('h'), low ('l'), and volume ('v')

        symbol: str symbol to get data
        timeframe: "minute", "1Min", "5Min", "15Min", "day", or "1D"
        limit: max number of bars to return 
        start: data must come at or after timestamp start
        end: data must come at or before timestamp end
        '''
        method = "/v1/bars/" + timeframe

        method += ("?symbols=" + symbol)
        method += ("&limit=" + str(limit))

        if start != None:
            method += ("&start=" + start)

        if end != None:
            method += ("&end=" + end)
        
        r = requests.get(data_domain + method, headers=self.__get_auth_header())
        code = r.status_code
        if code == 200:
            return list(json.loads(r.text)[symbol])
        else:
            print("Get data failed with error code " + str(code))
            print(r.text)
            return []
    

    def test_asset(self, symbol):
        method = "/v2/assets/"

        r = requests.get(core_domain + method + symbol, headers=self.__get_auth_header())
        code = r.status_code
        if code == 200:
            return True
        elif code == 404:
            return False
        else:
            print("????")
            return False

