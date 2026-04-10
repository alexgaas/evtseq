#include "interval_set.h"

extern "C" {
    typedef IntervalSet ES;

    ES* es_create() {
        return new ES();
    }

    void es_destroy(ES* event_set) {
        delete event_set;
    }

    void es_insert(ES* event_set, uint32_t event_time) {
        event_set->insert(event_time);
    }

    uint32_t es_get_sum_of_lengths(ES* event_set) {
        return event_set->getSumOfLengths();
    }

    uint32_t es_get_sum_of_squared_lengths(ES* event_set) {
        return event_set->getSumOfSquaredLengths();
    }

    uint32_t es_get_interval_between_events_count(ES* event_set) {
        return event_set->getIntervalBetweenEventsCount();
    }
}
