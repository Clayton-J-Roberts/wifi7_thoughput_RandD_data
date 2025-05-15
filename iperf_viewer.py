import json
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, simpledialog
import os
from datetime import datetime

def pick_files():
    root = Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(
        title="Select up to 3 JSON files",
        filetypes=[("JSON files", "*.json")]
    )
    return root, file_paths[:3]  # Return root window and selected files

def process_json(file_path, display_name):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        intervals = data.get("intervals", [])
        if not intervals:
            print(f"Warning: No intervals found in {file_path}")
            return None

        times = []
        bps = []
        interval_durations = []

        for i, interval in enumerate(intervals):
            try:
                start = interval["sum"]["start"]
                end = interval["sum"]["end"]
                duration = end - start
                interval_durations.append(duration)

                times.append(i + 1)
                throughput_mbps = interval["sum"]["bits_per_second"] / 1e6
                bps.append(throughput_mbps)
            except KeyError as e:
                print(f"Warning: Missing data in interval {i}: {e}")
                continue

        if not bps:
            print(f"Warning: No valid data points found in {file_path}")
            return None

        avg_throughput = sum(bps) / len(bps)
        degradation_percentage = ((bps[0] - bps[-1]) / bps[0]) * 100 if bps[0] != 0 else 0

        first_interval_duration = interval_durations[0]
        avg_interval_duration = sum(interval_durations) / len(interval_durations)
        total_test_duration = intervals[-1]["sum"]["end"]

        # Print and save summary
        summary_data = {
            "First interval duration": f"{first_interval_duration:.2f} sec",
            "Average interval duration": f"{avg_interval_duration:.2f} sec",
            "Total test duration": f"{total_test_duration:.2f} sec",
            "Average throughput": f"{avg_throughput:.2f} Mbps",
            "Throughput degradation": f"{degradation_percentage:.2f}%"
        }

        print(f"\nResults for {display_name}")
        summary_filename = f"{display_name}_summary.txt"
        with open(summary_filename, "w") as out:
            for key, value in summary_data.items():
                print(f"{key}: {value}")
                out.write(f"{key}: {value}\n")

        print(f"Saved summary to: {os.path.abspath(summary_filename)}")
        return times, bps, display_name

    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error processing {file_path}: {e}")
        return None

def plot_comparison(data_sets):
    try:
        plt.style.use('seaborn-v0_8-darkgrid')
        plt.figure(figsize=(15, 8))

        line_styles = ['-', '--', '-.']
        colors = ['#2196F3', '#E91E63', '#4CAF50']

        for i, (times, bps, label) in enumerate(data_sets):
            color = colors[i % len(colors)]
            linestyle = line_styles[i % len(line_styles)]

            plt.plot(times, bps,
                     marker='o',
                     label=label,
                     linestyle=linestyle,
                     color=color,
                     linewidth=2,
                     markersize=6)

            # Final point annotation
            plt.annotate(f"{label}",
                         xy=(times[-1], bps[-1]),
                         xytext=(5, 5),
                         textcoords='offset points',
                         fontsize=9,
                         color=color,
                         weight='bold')

            # Max/Min annotations
            max_val = max(bps)
            min_val = min(bps)
            max_idx = bps.index(max_val)
            min_idx = bps.index(min_val)
            percent_drop = ((max_val - min_val) / max_val) * 100 if max_val != 0 else 0

            plt.annotate(f"Max: {max_val:.1f} Mbps",
                         xy=(times[max_idx], max_val),
                         xytext=(0, 15),
                         textcoords='offset points',
                         arrowprops=dict(arrowstyle='->', color=color),
                         fontsize=8,
                         color=color)

            plt.annotate(f"Min: {min_val:.1f} Mbps\n↓ {percent_drop:.1f}%",
                         xy=(times[min_idx], min_val),
                         xytext=(0, -30),
                         textcoords='offset points',
                         arrowprops=dict(arrowstyle='->', color=color),
                         fontsize=8,
                         color=color)

            # Average line
            avg = sum(bps) / len(bps)
            plt.axhline(y=avg, color=color, linestyle='dotted', linewidth=1)
            plt.text(times[0] - 0.5, avg, f"Avg: {avg:.1f} Mbps", color=color, fontsize=8, va='bottom')

        plt.title("Network Throughput Comparison Over Time", fontsize=16, pad=20)
        plt.xlabel("Time Interval (seconds)", fontsize=12, labelpad=10)
        plt.ylabel("Throughput (Mbps)", fontsize=12, labelpad=10)
        plt.grid(True, which='major', linestyle='-', alpha=0.5)
        plt.grid(True, which='minor', linestyle=':', alpha=0.2)
        plt.minorticks_on()
        plt.legend(fontsize=10, bbox_to_anchor=(1.02, 1), loc='upper left')
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.tight_layout(rect=[0, 0, 0.95, 1])

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plot_filename = f"comparison_plot_{timestamp}.png"
        plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
        plt.show()
        plt.close()
        print(f"\nSaved comparison plot to: {os.path.abspath(plot_filename)}")
    except Exception as e:
        print(f"Error creating plot: {e}")

if __name__ == "__main__":
    root, selected_files = pick_files()
    if selected_files:
        results = []
        for i, file in enumerate(selected_files):
            name = simpledialog.askstring("Input", f"Enter a name for test file {i+1}:", parent=root)
            if name:
                result = process_json(file, name)
                if result:
                    results.append(result)
            else:
                print(f"No name entered for file {i+1}, skipping.")
        if results:
            plot_comparison(results)
    else:
        print("No files selected.")
    root.destroy()
