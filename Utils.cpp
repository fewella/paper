#include "Utils.hpp"

std::string Utils::get_orders_json() {
    json j;
    j["status"] = "all";

    std::string json_string = j.dump();
    return json_string;
    
}