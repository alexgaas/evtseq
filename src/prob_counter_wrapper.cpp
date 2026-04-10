#include "prob_counter.h"

extern "C" {
    typedef ProbabilisticCounter PC;

    PC* pc_create() {
        return new PC();
    }

    void pc_destroy(PC* counter) {
        delete counter;
    }

    void pc_increment(PC* counter) {
        counter->increment();
    }

    uint32_t pc_get_value(PC* counter) {
        return counter->getValue();
    }

    uint32_t pc_get_max_value() {
        return PC::MAX_VALUE;
    }
}
