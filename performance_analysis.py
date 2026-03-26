"""
CS 4310 - Operating Systems
Project #1: Performance Analysis

Runs all four scheduling algorithms over 20 random trials for each
input size (5, 10, 15 jobs) and writes results + graphs to outputs/.

"""

import random
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from schedulers import fcfs, sjf, read_jobs
from schedulers.rr import round_robin

# Constants
TRIALS      = 20
INPUT_SIZES = [5, 10, 15]
MAX_BURST   = 50
MIN_BURST   = 1
RANDOM_SEED = 42
OUTPUT_DIR  = os.path.join(os.path.dirname(__file__), "outputs")
GRAPHS_DIR  = os.path.join(OUTPUT_DIR, "graphs")

ALGO_NAMES = ["FCFS", "SJF", "RR-2", "RR-5"]
COLORS     = ["#2196F3", "#4CAF50", "#FF9800", "#E91E63"]
MARKERS    = ["o", "s", "^", "D"]


# Helpers

def generate_jobs(n, rng):
    return [(f"Job{i+1}", rng.randint(MIN_BURST, MAX_BURST)) for i in range(n)]

def avg_turnaround(results):
    return sum(r["turnaround"] for r in results) / len(results)

def run_all(jobs):
    f  = avg_turnaround(fcfs(jobs))
    s  = avg_turnaround(sjf(jobs))
    _, rr2 = round_robin(jobs, quantum=2)
    _, rr5 = round_robin(jobs, quantum=5)
    return f, s, avg_turnaround(rr2), avg_turnaround(rr5)


# Experiment

def run_experiment():
    rng = random.Random(RANDOM_SEED)
    all_data = {}
    for n in INPUT_SIZES:
        all_data[n] = [run_all(generate_jobs(n, rng)) for _ in range(TRIALS)]

    summary = {}
    for n in INPUT_SIZES:
        cols = list(zip(*all_data[n]))
        summary[n] = [sum(c) / TRIALS for c in cols]

    return all_data, summary


# Report

def write_report(all_data, summary):
    path = os.path.join(OUTPUT_DIR, "performance_results.txt")
    lines = [
        "CS 4310 Project #1 - Performance Analysis Results",
        "=" * 60,
        f"Trials per input size : {TRIALS}",
        f"Max burst time        : {MAX_BURST} ms",
        f"Random seed           : {RANDOM_SEED}",
        "",
    ]
    for n in INPUT_SIZES:
        lines += [
            f"--- Input Size: {n} jobs ---",
            f"{'Trial':<8} {'FCFS':>10} {'SJF':>10} {'RR-2':>10} {'RR-5':>10}",
            "-" * 52,
        ]
        for t, row in enumerate(all_data[n], 1):
            lines.append(f"{t:<8} {row[0]:>10.2f} {row[1]:>10.2f} {row[2]:>10.2f} {row[3]:>10.2f}")
        avgs = summary[n]
        lines += [
            "-" * 52,
            f"{'AVG':<8} {avgs[0]:>10.2f} {avgs[1]:>10.2f} {avgs[2]:>10.2f} {avgs[3]:>10.2f}",
            "",
        ]

    lines += [
        "=" * 60,
        "SUMMARY TABLE - Average of Average Turnaround Times (ms)",
        "=" * 60,
        f"{'Input Size':<14} {'FCFS':>10} {'SJF':>10} {'RR-2':>10} {'RR-5':>10}",
        "-" * 60,
    ]
    for n in INPUT_SIZES:
        a = summary[n]
        lines.append(f"{str(n)+' jobs':<14} {a[0]:>10.2f} {a[1]:>10.2f} {a[2]:>10.2f} {a[3]:>10.2f}")
    lines.append("=" * 60)

    with open(path, "w") as f:
        f.write("\n".join(lines))
    print(f"  Report  -> {path}")


# Graphs

def _style(ax, title):
    ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
    ax.set_xlabel("Number of Jobs", fontsize=11)
    ax.set_ylabel("Avg Turnaround Time (ms)", fontsize=11)
    ax.set_xticks(INPUT_SIZES)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

def plot_graphs(summary):
    # Individual graphs
    for idx, name in enumerate(ALGO_NAMES):
        y = [summary[n][idx] for n in INPUT_SIZES]
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(INPUT_SIZES, y, color=COLORS[idx], marker=MARKERS[idx],
                linewidth=2.2, markersize=8, label=name)
        for x, v in zip(INPUT_SIZES, y):
            ax.annotate(f"{v:.1f}", (x, v), textcoords="offset points",
                        xytext=(0, 8), ha="center", fontsize=9, color=COLORS[idx])
        _style(ax, f"{name} - Avg Turnaround vs Input Size")
        ax.legend()
        fig.tight_layout()
        out = os.path.join(GRAPHS_DIR, f"graph_{name.lower().replace('-','')}.png")
        fig.savefig(out, dpi=150)
        plt.close(fig)
        print(f"  Graph   -> {out}")

    # Combined graph
    fig, ax = plt.subplots(figsize=(8, 5))
    for idx, name in enumerate(ALGO_NAMES):
        y = [summary[n][idx] for n in INPUT_SIZES]
        ax.plot(INPUT_SIZES, y, color=COLORS[idx], marker=MARKERS[idx],
                linewidth=2.2, markersize=8, label=name)
    _style(ax, "All Algorithms - Avg Turnaround vs Input Size")
    ax.legend(loc="upper left", fontsize=10)
    fig.tight_layout()
    out = os.path.join(GRAPHS_DIR, "graph_combined.png")
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"  Graph   -> {out}")


# Entry

def run():
    os.makedirs(GRAPHS_DIR, exist_ok=True)
    print("\n[Performance Analysis]")
    print("  Running 20 trials x 3 input sizes x 4 algorithms ...")
    all_data, summary = run_experiment()
    write_report(all_data, summary)
    plot_graphs(summary)
    return summary


if __name__ == "__main__":
    run()