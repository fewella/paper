#include <nlohmann/json.hpp>
using json = nlohmann::json;

class Utils {
    public:
        // TODO: make custom parameters
        static std::string get_orders_json();
        static std::string post_order_json(std::string symbol, size_t n);
};
