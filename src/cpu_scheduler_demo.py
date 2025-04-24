
from dataclasses import dataclass, field
from typing import List, Dict
import sys

@dataclass(order=True)
class Process:
    pid: int
    arrival: int
    burst: int
    priority: int = field(default=0, compare=False)
    start: int = field(default=-1, compare=False)
    finish: int = field(default=0, compare=False)
    remaining: int = field(init=False, compare=False)

    def __post_init__(self):
        self.remaining = self.burst

# --- Workload Generators ---

def get_small_synthetic() -> List[Process]:
    """Return a small hard-coded test workload."""
    pass

def get_large_synthetic() -> List[Process]:
    """Return a larger synthetic workload."""
    pass

def get_edge_case_workloads() -> Dict[str, List[Process]]:
    """Return a dict of edge-case workloads."""
    pass

# --- Scheduling Algorithms ---

def fcfs_scheduler(procs: List[Process]) -> List[Process]:
    """First-Come, First-Served scheduler."""
    pass

def sjf_scheduler(procs: List[Process]) -> List[Process]:
    """Shortest Job First (non-preemptive) scheduler."""
    pass

def srtf_scheduler(procs: List[Process]) -> List[Process]:
    """Shortest Remaining Time First (preemptive) scheduler."""
    pass

def mlfq_scheduler(procs: List[Process], q1=4, q2=8) -> List[Process]:
    """Multi-Level Feedback Queue scheduler."""
    pass

# --- Metrics & Reporting ---

def compute_metrics(schedule: List[Process]) -> Dict[str, float]:
    """Compute performance metrics for a schedule."""
    pass

def print_schedule_and_metrics(name: str, schedule: List[Process]):
    """Print schedule order and metrics."""
    pass

def plot_comparison(results: Dict[str, Dict[str, float]]):
    """Plot comparison chart across algorithms."""
    pass

# --- Menu Interface ---

def run_menu():
    """Terminal menu loop for user interaction."""
    pass

if __name__ == "__main__":
    run_menu()
