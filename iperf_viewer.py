import json
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog

def pick_file():
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select JSON file",
        filetypes=[("JSON files", "*.json")]
    )
    return file_path

def process_json(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    intervals = data["intervals"]
    times = []
    bps = []

    for i, interval in enumerate(intervals):
        times.append(i + 1)
        bps.append(interval["sum"]["bits_per_second"] / 1e6)  # Mbps

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(times, bps, marker='o')
    plt.title(f"Throughput Over Time\n{file_path}")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Throughput (Mbps)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    selected_file = pick_file()
    if selected_file:
        process_json(selected_file)
    else:
        print("No file selected.")
