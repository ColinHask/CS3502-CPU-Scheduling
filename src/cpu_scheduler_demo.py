import os
import copy
import random
import sys
from dataclasses import dataclass, field
from typing import List, Dict

import matplotlib.pyplot as plt

# holds everything the simulator needs to know about one job
@dataclass(order=True)
class Process:
    pid: int               # unique process ID
    arrival: int           # arrival time into the ready queue
    burst: int             # total CPU time needed
    priority: int = field(default=0, compare=False)

    start: int = field(default=-1, compare=False)   # first time on CPU
    finish: int = field(default=0,  compare=False)  # completion time
    remaining: int = field(init=False, compare=False)

    def __post_init__(self):
        self.remaining = self.burst

#  Workload Generators --------------------------------------------------------

# hardcoded 4 process workload for small test
def small_workload() -> List[Process]:
    """4 easy-to-verify processes."""
    return [
        Process(1, 0, 8),

        Process(2, 1, 4),
        Process(3, 2, 9),
        Process(4, 3, 5),
    ]

# larger realistic workload to showcase performance differences
def large_workload() -> List[Process]:
    random.seed(42)

    return [
        Process(i + 1, random.randint(0, 10), random.randint(1, 20))
        for i in range(20)
    ]

# edge case workloads
def edge_workloads() -> Dict[str, List[Process]]:
    
    return {

        #no variance
        # All five jobs arrive at time 0 and need exactly 5 ticks each.
        # No variation in arrival or burst.
        "Identical": [Process(i + 1, 0, 5) for i in range(5)],

        #maximum variance
        # Four jobs with huge burst variance (1, 2, 100, 200).
        # Short jobs arrive after the long one has already started
        "ExtremeMix": [

            Process(1, 0, 100),
            Process(2, 1, 1),

            Process(3, 2, 200),
            Process(4, 3, 2),
        ],
    }


#  Scheduling Algorithms -----------------------------------------------------------

# first come first serve
# Non-preemptive run jobs in arrival order
# Simple fair by arrival, but long first job means everyone waits
def fcfs(procs: List[Process]) -> List[Process]:
    t = 0
    for p in sorted(procs, key=lambda x: x.arrival):
        t = max(t, p.arrival)
        p.start, t = t, t + p.burst

        p.finish = t
    return procs

# shortest job first
# Non-preemptive. pick ready job with smallest burst
# Lowest average wait if burst times are known. can starve long jobs
def sjf(procs: List[Process]) -> List[Process]:
    pending = sorted(procs, key=lambda x: x.arrival)
    ready, done, t = [], [], 0
    while pending or ready:

        while pending and pending[0].arrival <= t:
            ready.append(pending.pop(0))

        if not ready:

            t = pending[0].arrival
            continue
        ready.sort(key=lambda x: x.burst)
        p = ready.pop(0)
        p.start, t = t, t + p.burst

        p.finish = t
        done.append(p)
    return done

#  shortest remaining time first
# Pre-emptive SJF; always run job with least remaining CPU.
# Minimizes wait/turnaround; lots of context switches; needs remaining-time estimates.
def srtf(procs: List[Process]) -> List[Process]:
    pending = sorted(procs, key=lambda x: x.arrival)
    ready, done, t = [], [], 0
    while pending or ready:

        while pending and pending[0].arrival <= t:
            ready.append(pending.pop(0))
        if not ready:

            t = pending[0].arrival
            continue
        ready.sort(key=lambda x: x.remaining)
        p = ready[0]

        if p.start < 0:
            p.start = t
        p.remaining -= 1
        t += 1
        if p.remaining == 0:
            p.finish = t
            done.append(p)
            ready.pop(0)
    return done

#  Multi-Level Feedback Queue
# two RR queues: 4-tick quantum (Q1) if still running, demote to 8-tick quantum (Q2)
# adapts without burst knowledge, favors short tasks, prevents starvation
def mlfq(procs: List[Process], q1=4, q2=8) -> List[Process]:
    pending = sorted(procs, key=lambda x: x.arrival)
    q1q, q2q, done, t = [], [], [], 0
    while pending or q1q or q2q:

        while pending and pending[0].arrival <= t:
            q1q.append(pending.pop(0))
        if q1q:
            p = q1q.pop(0)
            if p.start < 0:

                p.start = t
            run = min(q1, p.remaining)
            p.remaining -= run
            t += run
            if p.remaining == 0:
                p.finish = t
                done.append(p)

            else:
                q2q.append(p)
        elif q2q:

            p = q2q.pop(0)
            run = min(q2, p.remaining)
            p.remaining -= run
            t += run
            if p.remaining == 0:
                p.finish = t
                done.append(p)

            else:
                q2q.append(p)
        else:
            t = pending[0].arrival
    return done

# name to function map
ALGORITHMS = {
    "FCFS": fcfs,
    "SJF": sjf,
    "SRTF": srtf,
    "MLFQ": mlfq,
}


# ── Metrics + Reporting ───────────────────────────────────────────────
def metrics(schedule: List[Process]) -> Dict[str, float]:
    """Return AWT, ATT, RT, throughput, and CPU utilization."""
    n = len(schedule)
    total_burst = sum(p.burst for p in schedule)
    makespan = max(p.finish for p in schedule) - min(p.arrival for p in schedule)

    return {
        "AWT": sum(p.start - p.arrival for p in schedule) / n,
        "ATT": sum(p.finish - p.arrival for p in schedule) / n,
        "RT":  sum(p.start - p.arrival for p in schedule) / n,
        "Throughput": n / makespan,
        "CPU Utilization (%)": (total_burst / makespan) * 100,
    }

# Prints timeline & metrics
def report(name: str, schedule: List[Process]) -> Dict[str, float]:
    print(f"\n=== {name} ===")
    for p in schedule:
        print(
            f"P{p.pid:02d}: arrival={p.arrival:2d}, "
            f"burst={p.burst:2d}, start={p.start:2d}, finish={p.finish:2d}"
        )

    m = metrics(schedule)
    for k, v in m.items():
        print(f"  {k:>18}: {v:.2f}")   # widen field for the longer label
    return m


def plot(all_metrics: Dict[str, Dict[str, float]], title: str, filename: str):
    """Save comparison bar chart into repos img/ directory."""

    labels = list(all_metrics.keys())

    metric_names = list(next(iter(all_metrics.values())).keys())

    fig, axes = plt.subplots(len(metric_names), 1, figsize=(8, 3.5 * len(metric_names)))
    for idx, m in enumerate(metric_names):
        axes[idx].bar(labels, [all_metrics[a][m] for a in labels])
        axes[idx].set_title(m)

    fig.suptitle(title)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    out_dir = os.path.join(os.path.dirname(__file__), "img")

    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, filename)


    plt.savefig(out_path)
    print(f"Chart saved to {out_path}")
    plt.close(fig)


#  Runner Helper --------------------------------------------------------------------------
def run_workload(workload: List[Process], workload_name: str):
    results = {}
    for alg_name, alg_fn in ALGORITHMS.items():

        schedule = alg_fn(copy.deepcopy(workload))

        results[alg_name] = report(alg_name, schedule)
    plot(results, workload_name, f"{workload_name}_comparison.png")


#  Menu ---------------------------------------------------------------------------------
def menu():
    while True:
        print(
            "\nCPU Scheduler Menu\n"
            "1) Small synthetic workload (4 processes)\n"
            "2) Large synthetic workload (20 processes)\n"
            "3) Edge-case workloads\n"
            "4) Exit\n"
        )
        choice = input("Select an option: ").strip()

        if choice == "1":
            run_workload(small_workload(), "Small")

        elif choice == "2":
            run_workload(large_workload(), "Large")
        elif choice == "3":
            for name, wl in edge_workloads().items():

                run_workload(wl, f"Edge_{name}")
        elif choice == "4":
            sys.exit(0)
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()
