#!/usr/bin/env python3
"""
SSE Task 11 - Contradiction: minimal runnable demo.

Demonstrates the technical contradiction
    "increase batch size -> throughput up, but latency up"
and the separation-based resolution (adaptive, priority-aware batching).

Model (small and explicit, discrete-event style):

  * 2 workers, a shared FIFO bulk backlog.
  * A worker pulls ONE batch of `batch_size` bulk jobs at a time and is
    COMMITTED to the whole batch (it cannot be interrupted).
  * An urgent job arrives at t = URGENT_AT. It may only start when some worker
    becomes free; it is then served alone (fast lane, batch = 1).
  * Bigger batch -> dispatch overhead paid less often -> throughput up, BUT a
    worker stays committed longer -> urgent job waits longer (head-of-line
    blocking). That coupling is the contradiction.

Run:  python3 dispatcher.py
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass
from typing import Dict, List

DISPATCH_OVERHEAD = 0.20   # paid once per batch
BULK_JOBS = 200            # large backlog
BULK_PROC = 0.30
URGENT_AT = 2.0            # urgent job arrives at t=2
URGENT_PROC = 0.30


@dataclass
class Job:
    ready_at: float
    proc_time: float
    job_id: int = 0


def simulate(batch_size: int, workers: int = 2) -> Dict[str, float]:
    bulk = [Job(0.0, BULK_PROC, i) for i in range(BULK_JOBS)]
    free_at = [0.0] * workers
    completion: List[float] = []
    urgent_done_at = None

    i = 0
    while i < len(bulk) or urgent_done_at is None:
        w = min(range(workers), key=lambda k: free_at[k])

        # If the urgent job has arrived and is still pending, a freed worker
        # takes IT (fast lane). Otherwise the worker takes a bulk batch.
        if urgent_done_at is None and free_at[w] >= URGENT_AT:
            t = free_at[w] + DISPATCH_OVERHEAD + URGENT_PROC
            free_at[w] = t
            urgent_done_at = t
            continue

        if i >= len(bulk):
            # no bulk left; just wait for the urgent job to be served
            free_at[w] = max(free_at[w], URGENT_AT) + DISPATCH_OVERHEAD + URGENT_PROC
            urgent_done_at = free_at[w]
            continue

        batch = bulk[i:i + batch_size]
        t = max(free_at[w], batch[0].ready_at) + DISPATCH_OVERHEAD
        for job in batch:
            t += job.proc_time
            completion.append(t)
        free_at[w] = t
        i += batch_size

    makespan = max(free_at + completion + [urgent_done_at or 0.0])
    n = len(bulk) + 1
    return {
        "batch_size": float(batch_size),
        "throughput": round(n / max(makespan, 1e-9), 2),
        "urgent_latency": round((urgent_done_at or 0.0) - URGENT_AT, 2),
    }


def adaptive_batch(priority: int, queue_depth: int) -> int:
    """Separation 'by condition': urgent -> tiny batch, bulk backlog -> big batch."""
    if priority <= 1:
        return 1
    if queue_depth > 50:
        return 8
    return 4


def main() -> None:
    print("Technical contradiction demo (controlling variable = batch size):")
    print(f"  {'batch':>5} {'throughput':>11} {'urgent_latency':>15}")
    for b in (1, 10, 40):
        r = simulate(b)
        print(f"  {int(r['batch_size']):>5} {r['throughput']:>11} "
              f"{r['urgent_latency']:>15}")
    print("  -> bigger batch: throughput up, but the urgent job waits longer")
    print("     (head-of-line blocking) = the technical contradiction.\n")

    print("Resolution (separation by condition): batch size becomes a function")
    print("of queue depth and job priority instead of a constant:")
    for depth in (5, 60):
        for pr in (1, 5):
            print(f"  queue_depth={depth:<3} priority={pr} -> batch={adaptive_batch(pr, depth)}")

    print("\nTakeaway: no single constant batch size maximizes both throughput and")
    print("latency/fairness; the contradiction is resolved by separating the two")
    print("requirements in time / space / scale / condition")
    print("(see ../diagrams/separation.mmd).")


if __name__ == "__main__":
    main()
