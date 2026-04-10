## EventSeq - Memory-Efficient Event & Activity Tracking

High-performance, memory-efficient data structures for tracking events and activity patterns.

### ProbabilisticCounter
Tracks very large counts (up to 2.6 billion) using probabilistic increments.
- 2 bytes per counter vs 8 bytes traditional (75% reduction)
- Maximum Likelihood Estimation for accurate estimates
- Increments become less likely as count grows
- See detailed [explanation](PROB_COUNTER_EXPLANATION.md)

### EventSet
Stores ordered event sequences using time diffs instead of full timestamps.
- 2 bytes per event vs 4 bytes traditional (50% reduction)
- Tracks intervals, sum of durations, event counts within 30-minute threshold
- See detailed [explanation](INTERVAL_SET_EXPLANATION.md)

### ActivityCounter
Tracks 24-hour activity using a compact bitset.
- 3 bytes per event vs 32+ bytes traditional (90%+ reduction)
- Hourly activity tracking, consecutive activity detection
- See detailed [explanation](ACTIVITY_COUNTER_EXPLANATION.md)

### Use Cases

- Session tracking
- Event time series analysis
- Daily activity monitoring
- Large-scale analytics backends
- Real-time data aggregation systems
