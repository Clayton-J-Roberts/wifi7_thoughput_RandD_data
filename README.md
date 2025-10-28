# 🛰️ WiFi 7 Throughput R&D Data

**Repository:** `wifi7_thoughput_RandD_data`  
**Authors:**  
- [Clayton-J-Roberts](https://github.com/Clayton-J-Roberts)  
- [James-Hodder](https://github.com/James-Hodder)  
- [Andrei Mamaradlo](https://github.com/andreimama)  
- [Iutoi Tauafiafi-Iutoi](https://github.com/Iutoi)  
- [Alvyn Beldua](https://github.com/alvyncb)  

**Project Type:** University R&D / Wireless Networking  
**Topic:** Wi-Fi 7 (802.11be) Throughput Measurement and Analysis  

---

## 📘 Overview

This repository contains experimental data, scripts, and configurations for a research and development (R&D) project studying **Wi-Fi 7 (802.11be)** throughput under various conditions.

The goal of this project is to measure and analyse **how distance, hardware setup, and environmental factors affect link throughput** in a controlled testing setup using real-world networking equipment.

---

## 📂 Repository Structure

wifi7_thoughput_RandD_data/
│

├── .idea/ # IDE configuration files (JetBrains etc.)

├── wifidata/ # Folder containing raw and processed Wi-Fi test data

├── hardware and software configs.txt # Hardware and software configuration notes

├── iperf_viewer.py # Python script for parsing/visualising iPerf throughput data

└── samba_monitor.sh # Shell script for monitoring Samba file-transfer throughput


---

## ⚙️ Description of Files

### `.idea/`
Contains IDE workspace and project metadata.  
> You can ignore this folder — it’s automatically created by JetBrains IDEs **PyCharm**.

---

### `wifidata/`
Stores **raw measurement data** and **processed results** from Wi-Fi 7 throughput experiments.  
Each dataset typically represents a different:
- Test distance  
- Environment (e.g., indoor, outdoor)  
- Configuration setup  

---

### `hardware and software configs.txt`
Documents the testing setup, including:
- Router, server, and client model numbers  
- Operating systems and driver versions  
- Configuration details used during testing  

Useful for replication, benchmarking, and comparison.

---

### `iperf_viewer.py`
Python script that:
- Parses throughput data (from **iPerf3** or similar tools)  
- Generates graphs, averages, and statistical summaries  
- Can be customised to handle multiple datasets or test conditions  

---

### `samba_monitor.sh`
Bash script used to:
- Monitor **Samba (SMB)** network throughput in real-time  
- Log file-transfer rates for real-world performance testing between server and client  

---

🧭 Acknowledgements

Auckland University of Technology (AUT) — Networking & Cybersecurity Department

Supervisors and academic staff supporting the Wi-Fi 7 R&D project

Open-source contributors of iPerf3 and Samba, used in the testing workflow

---

📧 Contact

Authors:
Clayton-J-Roberts
 • James-Hodder
 • Andrei Mamaradlo
 • Iutoi Tauafiafi-Iutoi
 • Alvyn Beldua

Project Purpose:
University coursework and independent R&D focused on Wi-Fi 7 throughput performance testing and data analysis.
