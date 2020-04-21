import requests
import json

domain = "https://paper-api.alpaca.markets"

class Core:

    def __init__(self):
        self.API_KEY = "PKBZJXADC72D0Z9B1TME"
        self.SECRET_KEY = "2YPuW7wK5UOLZwx3/Nn1NQXWVrjyNhNLVvCh5i87"


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

        r = requests.get(domain + method, headers=self.__get_auth_header())
        print(r.text)


    # defaults to sell, market
    # returns True on success, False on failure
    def place_order(self, symbol, n, side="sell", order_type="market", time_in_force="day", limit_price=-1, stop_price=-1, extended_hours=False):
        method = "/v2/orders"

        print("n: " + str(n))
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

        data = json.dumps(data)

        r = requests.post(domain + method, headers=self.__get_auth_header(), data=data)
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

        r = requests.delete(domain + method, headers=self.__get_auth_header())
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

        r = requests.delete(domain + method, headers=self.__get_auth_header())
        code = r.status_code
        if code == 200:
            print("ALL ORDERS cancelled successfully")
            return True
        else:
            print("Request failed with code: " + str(code))
            print(r.text)
            return False
        

    def get_assets(self):
        method = "/v2/positions"

        r = requests.get(domain + method, headers=self.__get_auth_header())
        code = r.status_code
        if code == 200:
            print("Retrieval successful")
            data = json.loads(r.text)
            return data
        else:
            print("Retrieval failed with code: " + str(code))
            print(r.text)
            return []