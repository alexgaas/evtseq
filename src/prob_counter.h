#pragma once

#include <deque>
#include <algorithm>

#include "rand.h"

// Precalculated arrays for ProbabilisticCounter.
// Gives a O(1) way to increment counter.
struct PrecalcedCounter{
    PrecalcedCounter(){
        for (size_t count = 0; count < (1 << 16); ++count){
            result[count] = 0;
            mult[count] = 1;
            uint64_t cur = 1 << (2 * 8 - 2);
            uint64_t sum = 0;

            for (int i = 0; sum < count; ++i){
                result[count] += std::min(cur, count - sum) * mult[count];
                sum += cur;
                mult[count] <<= 1;
                if (i & 1 && cur > 1)
                    cur >>= 1;
            }
            if (sum != count)
                mult[count] >>= 1;
        }
    }

    [[nodiscard]] uint32_t getResult(const uint16_t count) const{
        return result[count];
    }

    [[nodiscard]] uint32_t getMult(const uint64_t count) const{
        return mult[count];
    }

private:
    uint32_t result[1 << 16]{};
    uint32_t mult[1 << 16]{};
};

// Probabilistic counter based on the Maximum Likelihood Estimation (MLE) estimation
// Preserves values up to 2684305408.
// Algorithm:
// - count in [0 to 2^14)                                          - increment with probability 1
//    - count in [2^14 to 2^14+2^14)                               - increment with probability 1/2
//    - count in [2^14+2^14 to 2^14+2^14+2^13)                     - increment with probability 1/4
//    - count in [2^14+2^14+2^13 to 2^14+2^14+2^13+2^13)           - increment with probability 1/8
//    - count in [2^14+2^14+2^13+2^13 to 2^14+2^14+2^13+2^13+2^12) - increment with probability 1/16
class ProbabilisticCounter{
public:
    ProbabilisticCounter(): count(0){}

    void increment(){
        if (count < (1ULL << (sizeof(count) - 2)) ||
            (random.nextDouble() < 1.0 / precalced.getMult(count) && count < std::numeric_limits<decltype(count)>::max()))
            ++count;
    }

    [[nodiscard]] uint32_t getValue() const{
        return precalced.getResult(count);
    }

    static const uint32_t MAX_VALUE = 2684305408U;

    private:
    uint16_t count{};
    static ThreadSafeRandom random;

    static PrecalcedCounter precalced;
};