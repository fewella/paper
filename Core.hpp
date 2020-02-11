#include <iostream>
#include <string>

#include <curl/curl.h>

#include <nlohmann/json.hpp>

#include "Utils.hpp"

/**
 * API: Alpaca (https://alpaca.markets/)
 * Current API limit: 200 requests/minute (about 3 requests/second)
 */
class Core {
    public:
        /** 
         * Initializes curl and header required for all requests
         * NOTE: EVERY CALL TO initialize() MUST BE MATCHED WITH A CALL TO cleanup();
         */
        void initialize();


        /**
         * Cleans up curl and header as setup by initialize()
         * Must match with an initialize() call
         */
        void cleanup();

        /**
         * Makes initial request to Alpaca
         * @return true if successful, false otherwise
         */
        bool test_authenticate();


        /**
         * Gets all paper orders
         * @return 
         */
        void get_orders();

        /**
         * Places an order
         * @param symbol stock to be bought
         * @param n how many to buy
         * @return success (true) or failure (false)
         */
        bool post_order(std::string symbol, size_t n);

    private:
        std::string API_Key = "PKZVNC08423ETEYMSCUY";
        std::string Secret_Key = "bmvI/gROgrOPzhmRToWB48Odav/fIJl370XKSD/k";

        CURL* curl;
        struct curl_slist* header;
};

