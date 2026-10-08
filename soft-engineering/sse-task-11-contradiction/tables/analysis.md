# SSE Task 11 — Analysis tables

Standalone tables backing the solution in `../README.md`.

## T1. System / element / change

| Field | Value |
|---|---|
| Software system | Task/worker queue service (async job scheduler) |
| Goal of improvement | Higher throughput / worker utilization without losing responsiveness |
| Element to change | Dispatcher — dispatch **batch size** (jobs handed to a worker per cycle) |
| Change direction | Increase batch size |

## T2. Effects of the change

| Aspect | Desired effect | Undesired (negative) effect |
|---|---|---|
| Overhead | Fewer dispatch round-trips | — |
| Utilization | Workers stop starving between dispatches | — |
| Latency | — | Longer per-job wait (head-of-line blocking) |
| Fairness | — | Urgent / high-priority jobs queued behind a held batch |
| Failure mode | — | One slow job delays the whole batch; retries amplify it |

## T3. Contradiction card

| Field | Content |
|---|---|
| **Change** | Increase dispatch batch size |
| **Desired effect** | Throughput ↑, worker utilization ↑ |
| **Undesired effect** | Per-job latency ↑, head-of-line blocking, priority fairness ↓ |
| **Technical contradiction (TC)** | *If we will increase the dispatch batch size, then we will increase throughput and worker utilization, but this leads to increased per-job latency and head-of-line blocking for urgent jobs.* |
| **Physical contradiction (PC)** | *The batch must be LARGE (throughput) and SMALL (latency/fairness) at the same time.* |

## T4. Improvement parameters (TRIZ-style)

| Improving parameter | Worsening parameter | Shared controlling variable |
|---|---|---|
| Processing throughput / productivity | Latency / waiting time | Batch size |
| Worker utilization | Fairness / responsiveness | Batch size |

## T5. Separation-based resolution

| Principle | Mechanism | Effect on contradiction |
|---|---|---|
| Time | Adaptive batch size (large ↔ small over time) | Large when idling, small when urgent jobs appear |
| Space | Priority lanes / class-separated queues | Bulk keeps large batches, priority keeps batch=1 |
| Scale | Preemptable, yielding batches | Coarse dispatch, fine execution |
| Condition | `batch = f(queue depth, oldest age, priority)` | SLA-driven sizing |
