#include "Utils.hpp"

std::string Utils::get_orders_json() {
    json j;
    j["status"] = "all";

    
    return j.dump();;
}

std::string Utils::post_order_json(std::string symbol, size_t n) {
    json j;
    j["symbol"]          = symbol;
    j["qty"]             = std::to_string(n);
    j["side"]            = "buy";
    j["type"]            = "market";
    j["time_in_force"]   = "day";
    // j["limit_price"]     = 1000;
    // j["stop_price"]      = 1000;

    return j.dump();
}
