#pragma once

#include <deque>
#include <algorithm>

// Provides key activity in the 24 hours.
// For correct update must get a new event timestamp within previews event timestamp
class ActivityCounter{
public:
    ActivityCounter(){
        clear();
    }

    void update(const uint32_t time, const uint32_t last_time){
        if (time <= last_time)
            return;

        if (time - last_time >= DAY_DURATION_SECONDS)
            clear();
        else{
            int shift = convertToHours(time) - convertToHours(last_time);
            if (shift < 0)
                shift += DAY_DURATION_HOURS;
            if (shift)
                shiftRight(shift);
        }
        setHighestBit();
    }

    void clear(){
        memset(bitset, 0, sizeof bitset);
    }

    [[nodiscard]] uint8_t getLast24HoursActivity() const{
        return __builtin_popcount(getMask());
    }

    [[nodiscard]] uint8_t getLatestConsecutiveActivity() const{
        uint8_t result = 0;
        for (int i = 2; i >= 0; --i){
            if (bitset[i] < 0xFF){
                for (uint8_t mask = 0x80; bitset[i] & mask; mask >>= 1)
                    ++result;
                break;
            }
            result += 8;
        }
        return result;
    }

private:
    void shiftRight(int shift){
        uint32_t mask = getMask();
        mask >>= shift;
        bitset[0] = mask & 0xFF;
        bitset[1] = (mask >> 8) & 0xFF;
        bitset[2] = (mask >> 16) & 0xFF;
    }

    [[nodiscard]] uint32_t getMask() const{
        return bitset[0] | (bitset[1] << 8) | (bitset[2] << 16);
    }

    void setHighestBit(){
        bitset[2] |= 0x80;
    }

    static int convertToHours(uint32_t time){
        return static_cast<int>((time % DAY_DURATION_SECONDS) / HOUR_DURATION_SECONDS);
    }

    static const uint32_t DAY_DURATION_HOURS = 24;
    static const uint32_t HOUR_DURATION_SECONDS = 3600;
    static const uint32_t DAY_DURATION_SECONDS = DAY_DURATION_HOURS * HOUR_DURATION_SECONDS;

    // number of bytes in bitset
    static const size_t BITSET_SIZE = 3;

    uint8_t bitset[BITSET_SIZE]{};
};