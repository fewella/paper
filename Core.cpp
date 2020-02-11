#include "Core.hpp"

using std::cout;
using std::endl;

size_t write_callback(char *contents, size_t size, size_t nmemb, void *userp)
{
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

void Core::initialize() {
    curl = curl_easy_init();
}

bool Core::test_authenticate() {
    if (!curl) {
        initialize();
    }

    auto header = get_auth_header();
    
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, header);
    curl_easy_setopt(curl, CURLOPT_URL, "https://paper-api.alpaca.markets/v2/account");

    CURLcode res = curl_easy_perform(curl);

    curl_slist_free_all(header);
    curl_easy_cleanup(curl);
    curl = nullptr;
    
    return res == CURLE_OK;
}


void Core::get_orders() {
    if (!curl) {
        initialize();
    }

    auto header = get_auth_header();

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


    // TODO: PUT INTO CLEANUP FUNCTION
    curl_slist_free_all(header);
    curl_easy_cleanup(curl);
    curl = nullptr;
}

bool Core::post_order(std::string symbol, size_t n) {
    
}


struct curl_slist* Core::get_auth_header() {
    struct curl_slist* chunk = NULL;

    std::string api_key_header = std::string("APCA-API-KEY-ID: ") + API_Key;
    std::string secret_key_header = std::string("APCA-API-SECRET-KEY: ") + Secret_Key;

    chunk = curl_slist_append(chunk, api_key_header.c_str());
    chunk = curl_slist_append(chunk, secret_key_header.c_str());

    return chunk;
}

