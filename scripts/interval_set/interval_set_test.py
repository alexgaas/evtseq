try:
    from . import IntervalSet
except ImportError:
    from interval_set import IntervalSet

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from pathlib import Path


def main():
    print("=== IntervalSet Basic Test ===")

    # Constants
    THRESHOLD = 1800  # 30 minutes in seconds
    MAX_SIZE = 38  # Maximum number of events stored
    MAX_GAP = (1 << 16) - 1  # Maximum gap before eviction (18+ hours)

    # Test 1: Basic insertion and retrieval
    print("\nTest 1: Basic event insertion")
    event_set = IntervalSet()
    event_set.insert(1000)
    print(f"After first event: {event_set}")

    event_set.insert(1100)  # 100 seconds gap
    print(f"After second event (gap: 100s): {event_set}")
    print(f"  Sum of lengths: {event_set.get_sum_of_lengths()}")
    print(f"  Sum of squared lengths: {event_set.get_sum_of_squared_lengths()}")
    print(f"  Interval count: {event_set.get_interval_between_events_count()}")

    # Test 2: Multiple events within threshold (1800 seconds = 30 minutes)
    print("\nTest 2: Multiple events within 30-minute threshold")
    event_set = IntervalSet()
    times = [0, 100, 300, 600, 900, 1200, 1500, 1800]
    for t in times:
        event_set.insert(t)

    print(f"Inserted events at times: {times}")
    print(f"  Sum of lengths: {event_set.get_sum_of_lengths()}")
    print(f"  Sum of squared lengths: {event_set.get_sum_of_squared_lengths()}")
    print(f"  Interval count: {event_set.get_interval_between_events_count()}")

    # Test 3: Events with some above threshold
    print("\nTest 3: Events with gaps exceeding 30-minute threshold")
    event_set = IntervalSet()
    times = [0, 100, 300, 1800, 2000, 50000]  # Last gap is > 18 hours
    for t in times:
        event_set.insert(t)

    print(f"Inserted events at times: {times}")
    print(f"  Sum of lengths: {event_set.get_sum_of_lengths()}")
    print(f"  Sum of squared lengths: {event_set.get_sum_of_squared_lengths()}")
    print(f"  Interval count: {event_set.get_interval_between_events_count()}")

    # Plot 1: Memory efficiency - Time diffs storage vs event count
    print("\n=== Collecting Data for Plot 1: Time Diff Storage ===")
    event_indices_1 = []
    time_diffs_1 = []
    memory_savings = []

    event_set = IntervalSet()
    current_time = 0

    for i in range(1, MAX_SIZE + 1):
        # Add events with ~300 second intervals
        current_time += 300
        event_set.insert(current_time)

        event_indices_1.append(i)
        # Each time_shift is a uint16_t (2 bytes)
        bytes_used = i * 2
        time_diffs_1.append(bytes_used)

        # Memory saved compared to storing full timestamps (4 bytes each)
        full_storage = i * 4
        savings_percent = ((full_storage - bytes_used) / full_storage) * 100
        memory_savings.append(savings_percent)

        if i % 5 == 0 or i == MAX_SIZE:
            print(f"Events: {i:2d}, Bytes used: {bytes_used:3d}, Memory savings: {savings_percent:.1f}%")

    # Plot 2: Eviction process - Events added to 18+ hour gap
    print("\n=== Collecting Data for Plot 2: Eviction Process ===")
    event_indices_2 = []
    event_count_2 = []
    interval_sums = []
    interval_counts = []

    event_set = IntervalSet()
    base_time = 0
    gap = 300  # 5-minute gaps initially

    for i in range(1, 50):
        current_time = base_time + i * gap
        event_set.insert(current_time)

        event_indices_2.append(i)
        # Count approximate active events (rough estimate based on sum of lengths)
        sum_lengths = event_set.get_sum_of_lengths()
        approx_events = sum_lengths // gap if gap > 0 else 0
        event_count_2.append(min(approx_events + 1, MAX_SIZE))  # Cap at MAX_SIZE
        interval_sums.append(event_set.get_sum_of_lengths())
        interval_counts.append(event_set.get_interval_between_events_count())

        if i % 5 == 0 or i in [1, 49]:
            print(f"Event {i:2d}: Sum={interval_sums[-1]:5d}s, Count={interval_counts[-1]:2d}, Active≈{event_count_2[-1]:2d}")

    # Create two plots
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('IntervalSet: Memory Efficiency & Eviction Process', fontsize=14, fontweight='bold')

    # Plot 1: Memory efficiency through time diffs storage
    ax = axes[0]
    ax2 = ax.twinx()

    # Left axis: bytes used
    line1 = ax.plot(event_indices_1, time_diffs_1, 'o-', color='#1f77b4', linewidth=2.5,
                    markersize=6, markerfacecolor='#1f77b4', markeredgewidth=1.5, label='Bytes Used (uint16 diffs)')
    ax.set_xlabel('Event Count', fontsize=12, fontweight='bold')
    ax.set_ylabel('Storage (bytes)', fontsize=12, fontweight='bold', color='#1f77b4')
    ax.tick_params(axis='y', labelcolor='#1f77b4')
    ax.grid(True, alpha=0.3, linestyle='--')

    # Right axis: memory savings percentage
    line2 = ax2.plot(event_indices_1, memory_savings, 's-', color='#2ca02c', linewidth=2.5,
                     markersize=6, markerfacecolor='#2ca02c', markeredgewidth=1.5, label='Memory Savings %')
    ax2.set_ylabel('Memory Savings (%)', fontsize=12, fontweight='bold', color='#2ca02c')
    ax2.tick_params(axis='y', labelcolor='#2ca02c')
    ax2.set_ylim([30, 60])

    # Add reference line for MAX_SIZE
    ax.axvline(x=MAX_SIZE, color='red', linestyle='--', linewidth=2, alpha=0.7, label='MAX_SIZE (38)')
    ax.text(MAX_SIZE + 0.5, max(time_diffs_1) * 0.9, 'MAX_SIZE\n(38 events)', fontsize=9,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax.set_title('Plot 1: Time Diffs Storage - Memory Efficiency\n(Stores only gaps between events, not absolute timestamps)',
                 fontsize=11, pad=15)
    ax.set_xlim(0, MAX_SIZE + 2)

    # Combine legends
    lines1 = line1 + line2
    labels1 = [l.get_label() for l in lines1]
    ax.legend(lines1, labels1, loc='center left', fontsize=10, framealpha=0.95)

    # Plot 2: Eviction process
    ax = axes[1]
    ax2 = ax.twinx()

    # Left axis: interval sum
    line1 = ax.plot(event_indices_2, interval_sums, 'o-', color='#ff7f0e', linewidth=2.5,
                    markersize=5, markerfacecolor='#ff7f0e', markeredgewidth=1.5, label='Sum of Intervals (s)')
    ax.set_xlabel('Event Number', fontsize=12, fontweight='bold')
    ax.set_ylabel('Sum of Intervals (seconds)', fontsize=12, fontweight='bold', color='#ff7f0e')
    ax.tick_params(axis='y', labelcolor='#ff7f0e')

    # Right axis: interval count
    line2 = ax2.plot(event_indices_2, interval_counts, 's-', color='#d62728', linewidth=2.5,
                     markersize=5, markerfacecolor='#d62728', markeredgewidth=1.5, label='Interval Count')
    ax2.set_ylabel('Interval Count (# gaps within 30min)', fontsize=12, fontweight='bold', color='#d62728')
    ax2.tick_params(axis='y', labelcolor='#d62728')

    # Add threshold lines
    ax.axhline(y=THRESHOLD, color='green', linestyle=':', linewidth=2, alpha=0.6, label='30-min Threshold')
    ax.fill_between(event_indices_2, 0, THRESHOLD, alpha=0.1, color='green', label='Within Threshold')

    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_title('Plot 2: Eviction Process\n(Events added with 5-min gaps - older events evicted when gap > 18 hours)',
                 fontsize=11, pad=15)

    # Combine legends
    lines2 = line1 + line2
    labels2 = [l.get_label() for l in lines2]
    ax.legend(lines2, labels2, loc='upper left', fontsize=10, framealpha=0.95)

    plt.tight_layout()
    output_path = Path(__file__).parent / 'event_set_analysis.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\n✓ Plot saved as '{output_path}'")


if __name__ == "__main__":
    main()
