"""
CS 4310 - Operating Systems
Project #1: Job Scheduler Simulation
Algorithm: Round-Robin (RR)

Description:
    Simulates the Round-Robin CPU scheduling algorithm with a configurable
    time quantum. Used for both RR-2 (quantum=2) and RR-5 (quantum=5).
    All jobs arrive at time 0 and are placed in the ready queue in file order.
    The scheduler cycles through jobs, giving each a time slice of `quantum` ms.
    If a job's remaining burst exceeds the quantum, it is re-queued at the back.

Input:
    job.txt - alternating lines of job name and burst time (ms)
    quantum - time slice value passed as a command-line argument (default: 2)

Output:
    Schedule table showing each time slice, start/stop burst values,
    per-job turnaround times, and average turnaround time.

Usage:
    python rr.py [job_file] [quantum]
    e.g.: python rr.py job.txt 2
          python rr.py job.txt 5

"""

import sys
from collections import deque


def read_jobs(filename: str) -> list[tuple[str, int]]:
    """
    Read jobs from a file. Each job occupies two consecutive lines:
    line 1 = job name, line 2 = burst time in ms.

    Args:
        filename: path to the job input file

    Returns:
        List of (job_name, burst_time) tuples in file order.

    Raises:
        FileNotFoundError: if the file does not exist
        ValueError: if burst time is not a valid integer
    """
    jobs = []
    with open(filename, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    if len(lines) % 2 != 0:
        raise ValueError("Input file must have an even number of non-empty lines "
                         "(job name followed by burst time).")

    for i in range(0, len(lines), 2):
        name = lines[i]
        burst = int(lines[i + 1])
        jobs.append((name, burst))

    return jobs


def round_robin(jobs: list[tuple[str, int]], quantum: int) -> tuple[list[dict], list[dict]]:
    """
    Run the Round-Robin scheduling algorithm.

    Each job is given up to `quantum` ms of CPU time per turn.
    If remaining burst > quantum, the job re-enters the back of the queue.
    Completion time is recorded when remaining burst reaches 0.

    Args:
        jobs: list of (job_name, burst_time) tuples (arrival order)
        quantum: time slice in ms

    Returns:
        A tuple of:
          - timeline: list of execution-slice dicts (for Gantt/table display)
              keys: job, start, stop, burst_before, burst_after
          - summary:  list of per-job completion dicts
              keys: job, burst, finish, turnaround
    """
    # Build ready queue: (name, original_burst, remaining_burst)
    queue = deque()
    for name, burst in jobs:
        queue.append({"job": name, "burst": burst, "remaining": burst})

    current_time = 0
    timeline = []       
    finish_time = {}     

    while queue:
        item = queue.popleft()
        name = item["job"]
        remaining = item["remaining"]

        burst_before = remaining
        run_time = min(quantum, remaining)
        start = current_time
        stop = current_time + run_time
        remaining -= run_time

        timeline.append({
            "job": name,
            "start": start,
            "stop": stop,
            "burst_before": burst_before,
            "burst_after": remaining,
        })

        current_time = stop

        if remaining > 0:
            # Job not finished; re-queue at the back
            queue.append({"job": name, "burst": item["burst"], "remaining": remaining})
        else:
            # Job finished
            finish_time[name] = stop

    summary = []
    for name, burst in jobs:
        finish = finish_time[name]
        summary.append({
            "job": name,
            "burst": burst,
            "finish": finish,
            "turnaround": finish,
        })

    return timeline, summary


def print_results(timeline: list[dict], summary: list[dict], quantum: int) -> float:
    """
    Print the time-slice table and per-job summary, return avg turnaround.

    Args:
        timeline: list of execution-slice dicts from round_robin()
        summary: list of per-job completion dicts from round_robin()
        quantum: time slice used (for display)

    Returns:
        Average turnaround time.
    """
    label = f"ROUND-ROBIN (Quantum = {quantum} ms) SCHEDULE TABLE"
    print("=" * 70)
    print(label)
    print("=" * 70)
    print(f"{'Job':<10} {'Start':>7} {'Stop':>6} {'Burst Before':>14} {'Burst After':>12}")
    print("-" * 70)
    for s in timeline:
        print(f"{s['job']:<10} {s['start']:>7} {s['stop']:>6} "
              f"{s['burst_before']:>14} {s['burst_after']:>12}")

    print("\n" + "=" * 70)
    print("PER-JOB TURNAROUND SUMMARY")
    print("=" * 70)
    print(f"{'Job':<10} {'Burst':>6} {'Finish':>8} {'Turnaround':>12}")
    print("-" * 70)

    total = 0
    for r in summary:
        print(f"{r['job']:<10} {r['burst']:>6} {r['finish']:>8} {r['turnaround']:>12}")
        total += r["turnaround"]

    avg = total / len(summary)
    print("-" * 70)
    print(f"{'Average Turnaround Time':>40}  {avg:>10.2f} ms")
    print("=" * 70)
    return avg


def main():
    filename = "job.txt"
    quantum = 2

    if len(sys.argv) > 1:
        filename = sys.argv[1]
    if len(sys.argv) > 2:
        quantum = int(sys.argv[2])

    try:
        jobs = read_jobs(filename)
    except FileNotFoundError:
        print(f"Error: '{filename}' not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error reading input: {e}")
        sys.exit(1)

    print(f"\nLoaded {len(jobs)} job(s) from '{filename}'. Quantum = {quantum} ms.\n")
    timeline, summary = round_robin(jobs, quantum)
    avg = print_results(timeline, summary, quantum)
    print(f"\nRR-{quantum} Average Turnaround Time: {avg:.2f} ms\n")


if __name__ == "__main__":
    main()
