# CS3502-CPU-Scheduling
CPU Scheduling project for Project 2 (CS3502 Operating Systems)

# CPU-Scheduling Simulator (Python)

## Table of Contents
1. [Overview](#overview)  
2. [Features](#features)  
3. [Installation](#installation)  
4. [Usage](#usage)  
5. [Repository Layout](#repository-layout)  
6. [Extending the Simulator](#extending-the-simulator)  
7. [License](#license)

---

## Overview
This console-based simulator demonstrates four CPU-scheduling policies, calculates
core performance metrics, and saves bar-chart comparisons for each workload.

| Algorithm | Type | Notes |
|-----------|------|-------|
| **FCFS**  | Non-preemptive | First-Come, First-Served |
| **SJF**   | Non-preemptive | Shortest Job First |
| **SRTF**  | Preemptive     | Shortest Remaining Time First *(new)* |
| **MLFQ**  | Preemptive     | Two-level Multi-Level Feedback Queue *(new)* |

---

## Features
* **Self-contained menu:** select a workload → runs *all* algorithms, prints
  schedules & metrics, and saves a PNG chart in `img/`.
* **Built-in workloads**  
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
