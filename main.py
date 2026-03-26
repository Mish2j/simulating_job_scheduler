"""
CS 4310 - Operating Systems
Project #1: Main Runner

Usage:
    python main.py # run all algorithms on all input files + performance analysis
    python main.py --file inputs/jobs_5.txt # run all algorithms on a specific file
    python main.py --perf # run performance analysis only
    python main.py --help # show this help message
"""

import os
import sys
import argparse

from schedulers import fcfs, sjf, read_jobs
from schedulers.rr import round_robin, print_results as rr_print
from schedulers.fcfs import print_results as fcfs_print
from schedulers.sjf  import print_results as sjf_print


INPUTS_DIR = os.path.join(os.path.dirname(__file__), "inputs")
DEFAULT_FILES = [
    os.path.join(INPUTS_DIR, "jobs_5.txt"),
    os.path.join(INPUTS_DIR, "jobs_10.txt"),
    os.path.join(INPUTS_DIR, "jobs_15.txt"),
]

DIVIDER = "─" * 70


def run_scheduler_on_file(filepath: str):
    """Run all four scheduling algorithms on a single job file."""
    filename = os.path.basename(filepath)

    print(f"\n{'═' * 70}")
    print(f"  INPUT FILE: {filename}")
    print(f"{'═' * 70}")

    try:
        jobs = read_jobs(filepath)
    except FileNotFoundError:
        print(f"  ERROR: File not found: {filepath}")
        return
    except ValueError as e:
        print(f"  ERROR: {e}")
        return

    print(f"  Loaded {len(jobs)} job(s)\n")

    # ── FCFS 
    print(f"\n{'─' * 70}")
    print("  ALGORITHM 1: First-Come-First-Serve (FCFS)")
    print(f"{'─' * 70}")
    fcfs_results = fcfs(jobs)
    fcfs_avg = fcfs_print(fcfs_results)

    # ── SJF
    print(f"\n{'─' * 70}")
    print("  ALGORITHM 2: Shortest-Job-First (SJF)")
    print(f"{'─' * 70}")
    sjf_results = sjf(jobs)
    sjf_avg = sjf_print(sjf_results)

    # ── RR-2 
    print(f"\n{'─' * 70}")
    print("  ALGORITHM 3: Round-Robin (RR-2, quantum = 2 ms)")
    print(f"{'─' * 70}")
    rr2_timeline, rr2_summary = round_robin(jobs, quantum=2)
    rr2_avg = rr_print(rr2_timeline, rr2_summary, quantum=2)

    # ── RR-5 
    print(f"\n{'─' * 70}")
    print("  ALGORITHM 4: Round-Robin (RR-5, quantum = 5 ms)")
    print(f"{'─' * 70}")
    rr5_timeline, rr5_summary = round_robin(jobs, quantum=5)
    rr5_avg = rr_print(rr5_timeline, rr5_summary, quantum=5)

    # ── Comparison summary
    print(f"\n{'═' * 70}")
    print(f"  COMPARISON SUMMARY — {filename}")
    print(f"{'═' * 70}")
    results = [
        ("FCFS",  fcfs_avg),
        ("SJF",   sjf_avg),
        ("RR-2",  rr2_avg),
        ("RR-5",  rr5_avg),
    ]
    for name, avg in results:
        bar_len = int(avg / 3)
        bar = "|" * bar_len
        print(f"  {name:<6}  {avg:>7.2f} ms  {bar}")

    ranked = sorted(results, key=lambda x: x[1])
    print(f"\n  Best: {ranked[0][0]}  ({ranked[0][1]:.2f} ms)")
    print(f"  Worst: {ranked[-1][0]}  ({ranked[-1][1]:.2f} ms)")
    print(f"{'═' * 70}\n")


def run_performance():
    """Run the full performance analysis (20 trials x 3 sizes x 4 algorithms)."""
    from performance_analysis import run
    run()


def parse_args():
    parser = argparse.ArgumentParser(
        description="CS 4310 Project #1 - Job Scheduler Simulator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "--file", "-f",
        metavar="PATH",
        help="Run all algorithms on a specific job file"
    )
    parser.add_argument(
        "--perf", "-p",
        action="store_true",
        help="Run performance analysis only (20 trials, generates graphs)"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.perf:
        # Performance analysis only
        run_performance()

    elif args.file:
        # Single file mode
        run_scheduler_on_file(args.file)

    else:
        # Default: run all input files + performance analysis
        print("\n[Step 1/2] Running all schedulers on each input file ...")
        for filepath in DEFAULT_FILES:
            run_scheduler_on_file(filepath)

        print("\n[Step 2/2] Running performance analysis (20 trials each) ...")
        run_performance()

        print("\n All done! Check the outputs/ folder for results and graphs.\n")


if __name__ == "__main__":
    main()