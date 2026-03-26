"""
CS 4310 - Operating Systems
Project #1: Job Scheduler Simulation
Algorithm: First-Come-First-Serve (FCFS)

Description:
    Simulates the FCFS CPU scheduling algorithm.
    Jobs are executed in the order they arrive (as read from the input file).
    All jobs are assumed to arrive at time 0.

Input:
    job.txt - alternating lines of job name and burst time (ms)

Output:
    Schedule table showing execution order, start/stop times,
    turnaround times, and average turnaround time.

"""

import sys


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


def fcfs(jobs: list[tuple[str, int]]) -> list[dict]:
    """
    Run the FCFS scheduling algorithm.

    All jobs arrive at time 0 and are served in the order provided.
    Each job runs to completion before the next begins (non-preemptive).

    Args:
        jobs: list of (job_name, burst_time) tuples

    Returns:
        List of result dicts with keys:
            job - job name
            burst - original burst time (ms)
            start - time the job began execution
            finish - time the job completed
            turnaround - finish - arrival (arrival = 0 for all jobs)
    """
    results = []
    current_time = 0

    for name, burst in jobs:
        start = current_time
        finish = start + burst
        turnaround = finish

        results.append({
            "job": name,
            "burst": burst,
            "start": start,
            "finish": finish,
            "turnaround": turnaround,
        })

        current_time = finish

    return results


def print_results(results: list[dict]) -> float:
    """
    Print a formatted schedule table and return the average turnaround time.

    Args:
        results: list of result dicts produced by fcfs()

    Returns:
        Average turnaround time across all jobs.
    """
    print("=" * 65)
    print("FIRST-COME-FIRST-SERVE (FCFS) SCHEDULE TABLE")
    print("=" * 65)
    header = f"{'Job':<10} {'Burst':>6} {'Start':>7} {'Finish':>8} {'Turnaround':>12}"
    print(header)
    print("-" * 65)

    total_turnaround = 0
    for r in results:
        print(f"{r['job']:<10} {r['burst']:>6} {r['start']:>7} {r['finish']:>8} {r['turnaround']:>12}")
        total_turnaround += r["turnaround"]

    avg = total_turnaround / len(results)
    print("-" * 65)
    print(f"{'Average Turnaround Time':>45}  {avg:>10.2f} ms")
    print("=" * 65)
    return avg


def main():
    filename = "job.txt"
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    try:
        jobs = read_jobs(filename)
    except FileNotFoundError:
        print(f"Error: '{filename}' not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error reading input: {e}")
        sys.exit(1)

    print(f"\nLoaded {len(jobs)} job(s) from '{filename}'.\n")
    results = fcfs(jobs)
    avg = print_results(results)
    print(f"\nFCFS Average Turnaround Time: {avg:.2f} ms\n")


if __name__ == "__main__":
    main()
