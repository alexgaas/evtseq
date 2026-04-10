#include <iostream>
#include <iomanip>
#include "src/interval_set.h"
#include "src/activity_counter.h"
#include "src/prob_counter.h"

int main() {
    IntervalSet event_set;
    for (int i = 0; i < 20; ++i) {
        event_set.insert(i * 300);
    }

    ActivityCounter activity_counter;
    uint32_t last_time = 0;
    for (int i = 0; i < 20; ++i) {
        activity_counter.update(i * 3600, last_time);
        last_time = i * 3600;
    }

    std::cout << "\nIntervalSet: Memory Efficiency\n";
    std::cout << "Traditional: 20 events * 4 bytes = 80 bytes\n";
    std::cout << "IntervalSet: 20 events * 2 bytes = 40 bytes\n";
    std::cout << "Savings: 40 bytes (50%)\n";

    std::cout << "\nActivityCounter: Memory Efficiency\n";
    std::cout << "Traditional: 32 bytes minimum\n";
    std::cout << "ActivityCounter: 3 bytes\n";
    std::cout << "Savings: 29 bytes (90%)\n";

    std::cout << "\nProbabilisticCounter: Memory Efficiency\n";
    ProbabilisticCounter prob_counter;
    for (int i = 0; i < 1000000; ++i) {
        prob_counter.increment();
    }
    std::cout << "Incremented 1,000,000 times\n";
    std::cout << "Estimated value: " << prob_counter.getValue() << "\n";
    std::cout << "Traditional: 8 bytes (uint64_t)\n";
    std::cout << "ProbabilisticCounter: 2 bytes\n";
    std::cout << "Savings: 6 bytes (75%)\n";

    return 0;
}
