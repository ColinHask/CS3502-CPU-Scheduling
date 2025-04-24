
# CPU-Scheduling Simulator

## Table of Contents
1. [Overview](#overview)  
2. [Features](#features)  
3. [Installation](#installation)  
4. [Usage](#usage)  

---

## Overview
This console-based simulator demonstrates four CPU-scheduling policies, calculates
core performance metrics, and saves bar-chart comparisons for each workload.

| Algorithm | Type | Notes |
|-----------|------|-------|
| **FCFS**  | Non-preemptive | First-Come, First-Served |
| **SJF**   | Non-preemptive | Shortest Job First |
| **SRTF**  | Preemptive     | Shortest Remaining Time First |
| **MLFQ**  | Preemptive     | Two-level Multi-Level Feedback Queue |

---

## Features
* **Menu:** select a workload → runs *all* algorithms, prints
  schedules & metrics, and saves a PNG chart in `img/`.
* **Built in workloads**  
  * **Small** (4 processes) – sanity check  
  * **Large** (20 processes) – deterministic random seed  
  * **Edge cases** – identical bursts & extreme burst mix
* **Metrics collected**
  * Average Waiting Time (AWT)  
  * Average Turnaround Time (ATT)  
  * Response Time (RT)  
  * Throughput (proc / time)  
  * CPU Utilization (%)

---

## Installation
```bash
python -m venv venv
# Unix / macOS
source venv/bin/activate
# Windows
# venv\Scripts\activate
pip install -r requirements.txt
```
## Usage
```bash
python cpu_scheduler.py
```
Menu:
```
CPU Scheduler Menu
1) Small synthetic workload (4 processes)
2) Large synthetic workload (20 processes)
3) Edge-case workloads
4) Exit
```
Choosing **1**, **2**, or **3** will:
1. Load the workload  
2. Execute FCFS, SJF, SRTF, MLFQ  
3. Print schedules & metrics  
4. Save a comparison chart to `img/<WorkloadName>_comparison.png`

Example output:
```
=== SRTF ===
P01: arrival= 0, burst= 8, start= 0, finish=16
...
  AWT        : 4.50
  ATT        : 9.25
  RT         : 4.50
  Throughput : 0.24
  CPU_Util   : 100.00
Chart saved to img/Small_comparison.png
```