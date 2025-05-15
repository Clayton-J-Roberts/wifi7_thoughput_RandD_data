import json
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, simpledialog
import os

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
        plt.figure(figsize=(12, 6))
        for times, bps, label in data_sets:
            plt.plot(times, bps, marker='o', label=label)

        plt.title("Throughput Comparison")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Throughput (Mbps)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plot_filename = "comparison_plot.png"
        plt.savefig(plot_filename)
        plt.show()
        plt.close()  # Properly close the figure
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
    root.destroy()  # Clean up Tk window