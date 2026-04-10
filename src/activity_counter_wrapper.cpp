#include "activity_counter.h"

extern "C" {
    typedef ActivityCounter AC;

    AC* ac_create() {
        return new AC();
    }

    void ac_destroy(AC* counter) {
        delete counter;
    }

    void ac_update(AC* counter, uint32_t time, uint32_t last_time) {
        counter->update(time, last_time);
    }

    void ac_clear(AC* counter) {
        counter->clear();
    }

    uint8_t ac_get_last_24_hours_activity(AC* counter) {
        return counter->getLast24HoursActivity();
    }

    uint8_t ac_get_latest_consecutive_activity(AC* counter) {
        return counter->getLatestConsecutiveActivity();
    }
}
