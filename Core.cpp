#include "Core.hpp"

using std::cout;
using std::endl;

size_t write_callback(char *contents, size_t size, size_t nmemb, void *userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}


void Core::initialize() {
    curl = curl_easy_init();

    std::string api_key_header = std::string("APCA-API-KEY-ID: ") + API_Key;
    std::string secret_key_header = std::string("APCA-API-SECRET-KEY: ") + Secret_Key;

    header = curl_slist_append(header, api_key_header.c_str());
    header = curl_slist_append(header, secret_key_header.c_str());
}


void Core::cleanup() {
    curl_slist_free_all(header);
    curl_easy_cleanup(curl);

    curl = nullptr;
    header = nullptr;
}


bool Core::test_authenticate() {
    initialize();
    
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, header);
    curl_easy_setopt(curl, CURLOPT_URL, "https://paper-api.alpaca.markets/v2/account");

    CURLcode res = curl_easy_perform(curl);
    cleanup();
    
    return res == CURLE_OK;
}


void Core::get_orders() {
    initialize();

    std::string buffer;

    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, header);
    curl_easy_setopt(curl, CURLOPT_URL, "https://paper-api.alpaca.markets/v2/orders");
    curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "GET");

    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &buffer);

    //std::string order_json = Utils::get_orders_json();
    //curl_easy_setopt(curl, CURLOPT_POSTFIELDS, order_json.c_str());

    CURLcode res = curl_easy_perform(curl);
    cout << "buffer: " << buffer << endl;

    cleanup();
}

bool Core::post_order(std::string symbol, size_t n) {
    initialize();

    std::string order_json = Utils::post_order_json(symbol, n);
    std::string buffer;
    
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, header);
    curl_easy_setopt(curl, CURLOPT_URL, "https://paper-api.alpaca.markets/v2/orders");
    curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "POST");
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, order_json.c_str());

    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &buffer);

    CURLcode res = curl_easy_perform(curl);
    cout << "buffer: " << buffer << endl;

    cleanup();

    return res==CURLE_OK;
}


