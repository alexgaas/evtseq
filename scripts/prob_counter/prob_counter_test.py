try:
    from . import ProbabilisticCounter
except ImportError:
    from prob_counter import ProbabilisticCounter

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from pathlib import Path

def main():
    counter = ProbabilisticCounter()
    counter.increment()
    print(counter.get_value())  # Get estimated count
    print(ProbabilisticCounter.get_max_value())  # Get max value

    # Demonstrate MLE algorithm ranges
    # count in [0, 2^14) = [0, 16384) - increment with probability 1
    # count in [2^14, 2^14+2^14) = [16384, 32768) - increment with probability 1/2
    # count in [2^14+2^14, 2^14+2^14+2^13) = [32768, 49152) - increment with probability 1/4
    # count in [2^14+2^14+2^13, 2^14+2^14+2^13+2^13) = [49152, 65536) - increment with probability 1/8
    # count in [2^14+2^14+2^13+2^13, 2^14+2^14+2^13+2^13+2^12) - increment with probability 1/16

    print("\n=== MLE Algorithm Range Test ===")
    test_ranges = [
        ("Range 0: [0, 2^14)", 16384, 1000),
        ("Range 1: [2^14, 2^14+2^14)", 32768, 5000),
        ("Range 2: [2^14+2^14, 2^14+2^14+2^13)", 49152, 5000),
        ("Range 3: [2^14+2^14+2^13, 2^14+2^14+2^13+2^13)", 65536, 10000),
    ]

    # Collect data for plotting
    all_iterations = []
    all_values = []
    range_labels = []
    range_boundaries = []

    for label, target_count, sample_interval in test_ranges:
        counter = ProbabilisticCounter()
        print(f"\n{label}")
        print(f"Target iterations: {target_count}")

        iterations = []
        values = []

        for i in range(1, target_count + 1):
            counter.increment()
            if i % sample_interval == 0:
                value = counter.get_value()
                error = ((value - i) / i) * 100
                iterations.append(i)
                values.append(value)
                print(f"  Iterations: {i:7d}, Value: {value:7d}, Error: {error:+6.2f}%")

        all_iterations.append(iterations)
        all_values.append(values)
        range_labels.append(label.split(":")[0])
        range_boundaries.append(target_count)

    # Create single focused plot
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.suptitle('Probabilistic Counter: Estimated vs Real Values', fontsize=15, fontweight='bold')

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

    # Plot true count line (diagonal)
    all_x = []
    for iterations in all_iterations:
        all_x.extend(iterations)
    max_x = max(all_x)
    ax.plot([0, max_x], [0, max_x], 'k--', linewidth=2.5, alpha=0.4, label='Perfect Estimate (y=x)', zorder=1)

    # Plot counter values for each range
    for idx, (iterations, values, label, boundary) in enumerate(zip(all_iterations, all_values, range_labels, range_boundaries)):
        ax.plot(iterations, values, 'o-', color=colors[idx], label=label,
                markersize=6, linewidth=2, alpha=0.8, markeredgewidth=1, markeredgecolor='white', zorder=2)

        # Add range annotation
        mid_point = boundary / 2
        ax.axvline(x=boundary, color=colors[idx], linestyle=':', linewidth=1.5, alpha=0.5)

    ax.set_xlabel('Actual Increment Count', fontsize=13, fontweight='bold')
    ax.set_ylabel('Counter Estimated Value', fontsize=13, fontweight='bold')
    ax.set_title('Counter Accuracy Across MLE Algorithm Ranges', fontsize=12, pad=15)
    ax.legend(loc='upper left', fontsize=11, framealpha=0.95)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlim(0, max_x * 1.05)
    ax.set_ylim(0, max_x * 1.05)

    # Add text box explaining the ranges
    textstr = 'MLE Ranges:\n' + \
              'Range 0: P=1.0 (perfect accuracy)\n' + \
              'Range 1: P=1/2 (minimal error)\n' + \
              'Range 2: P=1/4 (small error)\n' + \
              'Range 3: P=1/8 (small error)'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax.text(0.98, 0.05, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='bottom', horizontalalignment='right', bbox=props, family='monospace')

    plt.tight_layout()
    output_path = Path(__file__).parent / 'mle_counter_analysis.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\n✓ Plot saved as '{output_path}'")

if __name__ == "__main__":
    main()
