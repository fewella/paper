#include "Core.hpp"

using std::cout;
using std::endl;

int main() {
    Core* core = new Core();

    //core->post_order("GOOG", 5);
    //core->get_orders();
    core->get_market_data();

    delete core;
}

