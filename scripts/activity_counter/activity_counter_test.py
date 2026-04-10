try:
    from . import ActivityCounter
except ImportError:
    from activity_counter import ActivityCounter

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from pathlib import Path


def main():
    print("=== ActivityCounter Basic Test ===")

    # Constants
    HOUR = 3600  # seconds
    DAY = 24 * HOUR

    # Test 1: Single hour activity
    print("\nTest 1: Single hour activity")
    counter = ActivityCounter()
    base_time = 0

    counter.update(base_time + HOUR, base_time)
    print(f"After update from hour 0 to hour 1:")
    print(f"  Activity in last 24h: {counter.get_last_24_hours_activity()} hours")
    print(f"  Consecutive activity: {counter.get_latest_consecutive_activity()} hours")

    # Test 2: Multiple consecutive hours
    print("\nTest 2: Multiple consecutive hours activity")
    counter = ActivityCounter()
    base_time = 0

    for i in range(5):
        counter.update(base_time + (i + 1) * HOUR, base_time + i * HOUR)

    print(f"After 5 consecutive hour updates:")
    print(f"  Activity in last 24h: {counter.get_last_24_hours_activity()} hours")
    print(f"  Consecutive activity: {counter.get_latest_consecutive_activity()} hours")

    # Test 3: Activity throughout the day
    print("\nTest 3: Activity scattered throughout the day")
    counter = ActivityCounter()
    base_time = 0
    active_hours = [0, 2, 5, 10, 15, 18, 23]

    for hour in active_hours:
        counter.update(base_time + (hour + 1) * HOUR, base_time + hour * HOUR)

    print(f"Activity at hours: {active_hours}")
    print(f"  Activity in last 24h: {counter.get_last_24_hours_activity()} hours")
    print(f"  Consecutive activity: {counter.get_latest_consecutive_activity()} hours")

    # Test 4: Day boundary crossing
    print("\nTest 4: Day boundary crossing (clears activity)")
    counter = ActivityCounter()
    base_time = 0

    # Add activity in first day
    counter.update(base_time + 5 * HOUR, base_time)

    print(f"After 5 hours of activity:")
    print(f"  Activity: {counter.get_last_24_hours_activity()} hours")

    # Cross day boundary - should clear
    counter.update(base_time + DAY + 2 * HOUR, base_time + 5 * HOUR)

    print(f"After crossing day boundary (gap >= 24h):")
    print(f"  Activity: {counter.get_last_24_hours_activity()} hours (cleared)")

    # Test 5: Synthetic test - Event eviction over time
    print("\n=== Synthetic Test: Event Eviction Over N Events ===")

    # Generate N events uniformly distributed over time
    N = 50
    counter = ActivityCounter()

    # Events distributed over 36 hours (1.5 days) - will trigger eviction after 24 hours
    total_duration = 36 * HOUR
    event_times = []
    total_activity_list = []
    consecutive_activity_list = []
    event_indices = []

    base_time = 0
    last_time = base_time

    for i in range(N):
        # Uniformly distribute events over total_duration
        current_time = base_time + (i / N) * total_duration
        event_times.append(current_time)

        # Update counter
        counter.update(int(current_time), int(last_time))
        last_time = current_time

        # Record metrics every 5 events for cleaner plot
        if i % 5 == 0 or i == N - 1:
            event_indices.append(i + 1)
            total_activity_list.append(counter.get_last_24_hours_activity())
            consecutive_activity_list.append(counter.get_latest_consecutive_activity())

            # Print progress
            hours_elapsed = (current_time - base_time) / HOUR
            print(f"Event {i + 1:2d} (t={hours_elapsed:6.2f}h): "
                  f"Total activity={counter.get_last_24_hours_activity():2d}h, "
                  f"Consecutive={counter.get_latest_consecutive_activity():2d}h")

    # Create single plot showing event eviction
    fig, ax = plt.subplots(figsize=(12, 7))
    fig.suptitle(f'ActivityCounter: Event Eviction Over {N} Events (36-hour simulation)',
                 fontsize=14, fontweight='bold')

    # Plot total activity and consecutive activity
    ax.plot(event_indices, total_activity_list, 'o-', color='#1f77b4',
            label='Total Activity Hours', linewidth=2.5, markersize=7, markerfacecolor='#1f77b4', markeredgewidth=1.5)
    ax.plot(event_indices, consecutive_activity_list, 's-', color='#ff7f0e',
            label='Consecutive Activity Hours', linewidth=2.5, markersize=7, markerfacecolor='#ff7f0e', markeredgewidth=1.5)

    # Add vertical line at 24-hour mark to show eviction point
    eviction_event = int((24 / 36) * N)
    if eviction_event < N:
        ax.axvline(x=eviction_event, color='red', linestyle='--', linewidth=2, alpha=0.7, label='24-hour eviction point')
        ax.text(eviction_event, ax.get_ylim()[1] * 0.95, f'Eviction\n(event ~{eviction_event})',
                ha='center', fontsize=10, color='red', fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax.set_xlabel('Event Number', fontsize=12, fontweight='bold')
    ax.set_ylabel('Activity Hours', fontsize=12, fontweight='bold')
    ax.set_title('Activity Accumulation and Eviction as Events Progress in Time', fontsize=12, pad=20)
    ax.legend(loc='upper right', fontsize=11, framealpha=0.95)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlim(0, N)

    plt.tight_layout()
    output_path = Path(__file__).parent / 'activity_counter_analysis.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\n✓ Plot saved as '{output_path}'")


if __name__ == "__main__":
    main()
