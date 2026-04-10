#pragma once

#include <deque>
#include <algorithm>

// Preserves event sequence ordered in time.
// To save a memory class only stores time diff between neighbor events.
// uint16_t allows diff between two neighbor events longer events no longer than 18 hours.
// If gap between events more than 18 hours - earlier events are evicted.
// Class supports squared sum between events in line behind no longer than INTERVAL_THRESHOLD seconds.
class IntervalSet{
public:
    IntervalSet(): min_time(0), sum_of_lengths(0), sum_of_squared_lengths(0), interval_between_events_count(0){
        clear();
    }

    void insert(const uint32_t event_time)
    {
        if (min_time == 0){
            min_time = event_time;
            return;
        }

        const size_t size = getSize();

        if (event_time <= min_time){
            if (event_time == min_time){
                updateIntervalBetweenEventsCount(0);
                return;
            }
            if (size == MAX_SIZE || isWayEarlier(event_time, min_time))
                return;

            shiftRight(size);
            time_shifts[0] = min_time - event_time;
            min_time = event_time;
            updateSums(time_shifts[0], +1);
            updateIntervalBetweenEventsCount(time_shifts[0]);
            return;
        }

        uint32_t previous = min_time;
        for (size_t i = 0; i < size; ++i){
            uint32_t current = previous + time_shifts[i];
            if (current == event_time){
                updateIntervalBetweenEventsCount(0);
                return;
            }
            if (current > event_time){
                uint32_t old_interval = time_shifts[i];
                uint32_t new_interval_first = event_time - previous;
                uint32_t new_interval_second = current - event_time;

                if (size == MAX_SIZE){
                    if (i == 0){
                        min_time = event_time;
                        time_shifts[0] = new_interval_second;
                    }
                    else{
                        min_time += time_shifts[0];
                        shiftLeft(i - 1);
                        time_shifts[i - 1] = new_interval_first;
                        time_shifts[i] = new_interval_second;
                    }
                }
                else{
                    shiftRight(size);
                    shiftLeft(i);
                    time_shifts[i] = new_interval_first;
                    time_shifts[i + 1] = new_interval_second;
                }

                updateSums(old_interval, -1);
                updateSums(new_interval_first, +1);
                updateSums(new_interval_second, +1);
                updateIntervalBetweenEventsCount(old_interval, new_interval_first, new_interval_second);
                return;
            }
            previous = current;
        }

        if (isWayEarlier(previous, event_time)){
            clear();
            min_time = event_time;
            return;
        }

        uint32_t new_interval = event_time - previous;

        if (size == MAX_SIZE){
            min_time += time_shifts[0];
            shiftLeft(size - 1);
            time_shifts[size - 1] = new_interval;
        }
        else
            time_shifts[size] = new_interval;

        updateSums(new_interval, +1);
        updateIntervalBetweenEventsCount(new_interval);
    }

    [[nodiscard]] uint32_t getSumOfLengths() const{
        return sum_of_lengths;
    }

    [[nodiscard]] uint32_t getSumOfSquaredLengths() const{
        return sum_of_squared_lengths;
    }

    [[nodiscard]] uint32_t getIntervalBetweenEventsCount() const{
        return interval_between_events_count;
    }

private:
    // Calculate number of events to not store a size
    [[nodiscard]] size_t getSize() const{
        size_t size = 0;
        while (size < MAX_SIZE && time_shifts[size] != 0)
            ++size;
        return size;
    }

    // shift elements from position [0, last] to left, evicting 0-is element
    void shiftLeft(const size_t last){
        for (size_t i = 0; i + 1 <= last; ++i)
            time_shifts[i] = time_shifts[i + 1];
    }

    // shift elements from position [0, size - 1] to position [1, size]
    void shiftRight(const size_t size){
        for (size_t i = size; i >= 1; --i)
            time_shifts[i] = time_shifts[i - 1];
    }

    // verify time range of 18 hours passed
    static bool isWayEarlier(const uint32_t less_time, const uint32_t greater_time) {
        return greater_time > less_time + std::numeric_limits<uint16_t>::max();
    }

    void clear(){
        memset(time_shifts, 0, sizeof time_shifts);
    }

    void updateSums(uint32_t time_shift, int sign){
        if (time_shift <= INTERVAL_THRESHOLD){
            sum_of_lengths += time_shift * sign;
            sum_of_squared_lengths += time_shift * static_cast<uint64_t>(time_shift) * sign;
        }
    }

    void updateIntervalBetweenEventsCount(uint32_t old_interval, uint32_t new_interval_first, uint32_t new_interval_second){
        if (old_interval <= INTERVAL_THRESHOLD && interval_between_events_count < std::numeric_limits<uint32_t>::max())
            ++interval_between_events_count;
        else{
            updateIntervalBetweenEventsCount(new_interval_first);
            updateIntervalBetweenEventsCount(new_interval_second);
        }
    }

    void updateIntervalBetweenEventsCount(uint32_t new_interval){
        if (new_interval <= INTERVAL_THRESHOLD && interval_between_events_count <std::numeric_limits<uint32_t>::max())
            ++interval_between_events_count;
    }

    static const size_t MAX_SIZE = 38;
    static const uint16_t INTERVAL_THRESHOLD = 1800;

    uint32_t min_time;
    uint32_t time_shifts[MAX_SIZE]{};

    uint32_t sum_of_lengths;
    uint32_t sum_of_squared_lengths;

    // Count of intervals no longer than INTERVAL_THRESHOLD seconds between neighbor events
    uint32_t interval_between_events_count;
};