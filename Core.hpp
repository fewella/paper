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
         * Initializes curl
         */
        void initialize();

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

        /**
         * Returns required header to authenticate api requests
         * Note: must be cleaned up by calling function
         * @return struct curl_slist* with required keys
         */
        struct curl_slist* get_auth_header();
};

