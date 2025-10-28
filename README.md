# 🛰️ WiFi 7 Throughput R&D Data

**Repository:** `wifi7_thoughput_RandD_data`  
**Author:** [Clayton-J-Roberts](https://github.com/Clayton-J-Roberts)  
**Project Type:** University R&D / Wireless Networking  
**Topic:** Wi-Fi 7 (802.11be) Throughput Measurement and Analysis  
**Licence:** *(Add your licence, e.g. MIT or Creative Commons)*

---

## 📘 Overview
This repository contains experimental data, scripts, and configurations for a research and development (R&D) project studying **Wi-Fi 7 (802.11be)** throughput under various conditions.  

The project’s goal is to measure and analyse **how distance, hardware setup, and environment affect link throughput** in a controlled testing setup using real-world equipment.

---

## 📂 Repository Structure

**
---

## ⚙️ Description of Files

### `.idea/`
Contains IDE workspace and project metadata.  
> You can ignore this folder — it’s automatically created by JetBrains IDEs like PyCharm or IntelliJ.

### `wifidata/`
Stores **raw measurement data** and **processed results** from Wi-Fi 7 throughput experiments.  
Each dataset typically represents a different distance, environment, or configuration setup.

### `hardware and software configs.txt`
Documents:
- Router, server, and client model numbers  
- Operating systems and driver versions  
- Firmware or configuration details used during testing  

Useful for replication and comparison.

### `iperf_viewer.py`
Python script that:
- Parses throughput data (from iPerf3 or similar logs)  
- Generates graphs or statistics  
- Can be customised for multiple test datasets  

### `samba_monitor.sh`
Bash script used to:
- Monitor **Samba (SMB)** network throughput in real-time  
- Log transfer rates when testing file-copy performance between devices  

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Clayton-J-Roberts/wifi7_thoughput_RandD_data.git
cd wifi7_thoughput_RandD_data
**

