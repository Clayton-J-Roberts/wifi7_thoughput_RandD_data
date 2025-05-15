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
    return file_paths[:3]  # Limit to 3

def process_json(file_path, display_name):
    with open(file_path, "r") as f:
        data = json.load(f)

    intervals = data["intervals"]
    times = []
    bps = []
    interval_durations = []

    for i, interval in enumerate(intervals):
        start = interval["sum"]["start"]
        end = interval["sum"]["end"]
        duration = end - start
        interval_durations.append(duration)

        times.append(i + 1)
        throughput_mbps = interval["sum"]["bits_per_second"] / 1e6
        bps.append(throughput_mbps)

    avg_throughput = sum(bps) / len(bps)
    degradation_percentage = ((bps[0] - bps[-1]) / bps[0]) * 100 if bps[0] != 0 else 0

    first_interval_duration = interval_durations[0]
    avg_interval_duration = sum(interval_durations) / len(interval_durations)
    total_test_duration = intervals[-1]["sum"]["end"]

    # Print summary
    print(f"\nResults for {display_name}")
    print(f"First interval duration: {first_interval_duration:.2f} sec")
    print(f"Average interval duration: {avg_interval_duration:.2f} sec")
    print(f"Total test duration: {total_test_duration:.2f} sec")
    print(f"Average throughput: {avg_throughput:.2f} Mbps")
    print(f"Throughput degradation from start to end: {degradation_percentage:.2f}%")

    # Save summary
    summary_filename = f"{display_name}_summary.txt"
    with open(summary_filename, "w") as out:
        out.write(f"First Interval Duration: {first_interval_duration:.2f} sec\n")
        out.write(f"Average Interval Duration: {avg_interval_duration:.2f} sec\n")
        out.write(f"Total Test Duration: {total_test_duration:.2f} sec\n")
        out.write(f"Average Throughput: {avg_throughput:.2f} Mbps\n")
        out.write(f"Throughput Degradation: {degradation_percentage:.2f}%\n")

    print(f"Saved summary to: {os.path.abspath(summary_filename)}")

    return times, bps, display_name  # for plotting

def plot_comparison(data_sets):
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
    print(f"\nSaved comparison plot to: {os.path.abspath(plot_filename)}")

if __name__ == "__main__":
    selected_files = pick_files()
    if selected_files:
        results = []
        for i, file in enumerate(selected_files):
            root = Tk()
            root.withdraw()
            name = simpledialog.askstring("Input", f"Enter a name for test file {i+1}:")
            if name:
                result = process_json(file, name)
                results.append(result)
            else:
                print(f"No name entered for file {i+1}, skipping.")
        if results:
            plot_comparison(results)
    else:
        print("No files selected.")
