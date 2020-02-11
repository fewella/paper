#include "Core.hpp"

using std::cout;
using std::endl;

void init();
void close();

int main() {

    Core* core = new Core();

    core->get_orders();

    delete core;
}

