"""Discrete-event CPU scheduling simulator.

Algorithms:
- FCFS
- SJF (non-preemptive)
- SRTF (preemptive)
- Priority (non-preemptive)
- Round Robin
"""

from __future__ import annotations

from dataclasses import dataclass
from collections import deque
from typing import Iterable


@dataclass(frozen=True)
class Process:
    name: str
    arrival: int
    burst: int
    priority: int = 0

    def __post_init__(self):
        if self.arrival < 0:
            raise ValueError("arrival time must be >= 0")
        if self.burst <= 0:
            raise ValueError("burst time must be > 0")


@dataclass
class Result:
    name: str
    arrival: int
    burst: int
    priority: int
    completion: int = 0
    first_start: int | None = None

    @property
    def turnaround(self) -> int:
        return self.completion - self.arrival

    @property
    def waiting(self) -> int:
        return self.turnaround - self.burst

    @property
    def response(self) -> int:
        if self.first_start is None:
            raise RuntimeError("process has not started")
        return self.first_start - self.arrival


@dataclass(frozen=True)
class Segment:
    name: str
    start: int
    end: int


def _prepare(processes: Iterable[Process]) -> list[Process]:
    items = list(processes)
    if not items:
        raise ValueError("at least one process is required")
    if len({p.name for p in items}) != len(items):
        raise ValueError("process names must be unique")
    return sorted(items, key=lambda p: (p.arrival, p.name))


def _results(processes: list[Process], starts: dict[str, int], completion: dict[str, int]) -> list[Result]:
    return [
        Result(
            p.name, p.arrival, p.burst, p.priority,
            completion=completion[p.name],
            first_start=starts[p.name],
        )
        for p in processes
    ]


def fcfs(processes: Iterable[Process]) -> tuple[list[Result], list[Segment]]:
    ps = _prepare(processes)
    t = 0
    starts, completion = {}, {}
    segments = []
    for p in ps:
        if t < p.arrival:
            t = p.arrival
        starts[p.name] = t
        segments.append(Segment(p.name, t, t + p.burst))
        t += p.burst
        completion[p.name] = t
    return _results(ps, starts, completion), segments


def sjf(processes: Iterable[Process]) -> tuple[list[Result], list[Segment]]:
    ps = _prepare(processes)
    remaining = ps[:]
    t = 0
    starts, completion = {}, {}
    segments = []
    while remaining:
        available = [p for p in remaining if p.arrival <= t]
        if not available:
            t = min(p.arrival for p in remaining)
            continue
        p = min(available, key=lambda x: (x.burst, x.arrival, x.name))
        remaining.remove(p)
        starts[p.name] = t
        segments.append(Segment(p.name, t, t + p.burst))
        t += p.burst
        completion[p.name] = t
    return _results(ps, starts, completion), segments


def srtf(processes: Iterable[Process]) -> tuple[list[Result], list[Segment]]:
    ps = _prepare(processes)
    remaining = {p.name: p.burst for p in ps}
    by_name = {p.name: p for p in ps}
    t = min(p.arrival for p in ps)
    starts, completion = {}, {}
    segments: list[Segment] = []
    current: str | None = None
    seg_start = t

    while any(left > 0 for left in remaining.values()):
        available = [
            by_name[name] for name, left in remaining.items()
            if left > 0 and by_name[name].arrival <= t
        ]
        if not available:
            t = min(by_name[name].arrival for name, left in remaining.items() if left > 0)
            current = None
            seg_start = t
            continue

        p = min(available, key=lambda x: (remaining[x.name], x.arrival, x.name))
        if current != p.name:
            if current is not None and seg_start < t:
                segments.append(Segment(current, seg_start, t))
            current = p.name
            seg_start = t
            starts.setdefault(p.name, t)

        remaining[p.name] -= 1
        t += 1
        if remaining[p.name] == 0:
            completion[p.name] = t
            if seg_start < t:
                segments.append(Segment(p.name, seg_start, t))
            current = None
            seg_start = t

    return _results(ps, starts, completion), _merge_segments(segments)


def priority(processes: Iterable[Process]) -> tuple[list[Result], list[Segment]]:
    ps = _prepare(processes)
    remaining = ps[:]
    t = 0
    starts, completion = {}, {}
    segments = []
    while remaining:
        available = [p for p in remaining if p.arrival <= t]
        if not available:
            t = min(p.arrival for p in remaining)
            continue
        p = min(available, key=lambda x: (x.priority, x.arrival, x.name))
        remaining.remove(p)
        starts[p.name] = t
        segments.append(Segment(p.name, t, t + p.burst))
        t += p.burst
        completion[p.name] = t
    return _results(ps, starts, completion), segments


def round_robin(processes: Iterable[Process], quantum: int) -> tuple[list[Result], list[Segment]]:
    if quantum <= 0:
        raise ValueError("quantum must be > 0")
    ps = _prepare(processes)
    by_name = {p.name: p for p in ps}
    remaining = {p.name: p.burst for p in ps}
    t = 0
    index = 0
    ready: deque[str] = deque()
    starts, completion = {}, {}
    segments = []

    while len(completion) < len(ps):
        while index < len(ps) and ps[index].arrival <= t:
            ready.append(ps[index].name)
            index += 1

        if not ready:
            if index < len(ps):
                t = max(t, ps[index].arrival)
                continue
            break

        name = ready.popleft()
        p = by_name[name]
        starts.setdefault(name, t)
        run = min(quantum, remaining[name])
        segments.append(Segment(name, t, t + run))
        t += run
        remaining[name] -= run

        while index < len(ps) and ps[index].arrival <= t:
            ready.append(ps[index].name)
            index += 1

        if remaining[name] > 0:
            ready.append(name)
        else:
            completion[name] = t

    return _results(ps, starts, completion), _merge_segments(segments)


def _merge_segments(segments: list[Segment]) -> list[Segment]:
    merged: list[Segment] = []
    for s in segments:
        if merged and merged[-1].name == s.name and merged[-1].end == s.start:
            merged[-1] = Segment(s.name, merged[-1].start, s.end)
        else:
            merged.append(s)
    return merged


ALGORITHMS = {
    "fcfs": fcfs,
    "sjf": sjf,
    "srtf": srtf,
    "priority": priority,
}


def simulate(name: str, processes: Iterable[Process], quantum: int = 2):
    name = name.lower()
    if name == "rr":
        return round_robin(processes, quantum)
    if name not in ALGORITHMS:
        raise ValueError(f"unknown algorithm: {name}")
    return ALGORITHMS[name](processes)


def averages(results: list[Result]) -> dict[str, float]:
    n = len(results)
    return {
        "waiting": sum(r.waiting for r in results) / n,
        "turnaround": sum(r.turnaround for r in results) / n,
        "response": sum(r.response for r in results) / n,
    }


def cpu_utilisation(processes: Iterable[Process], segments: list[Segment]) -> float:
    ps = list(processes)
    first = min(p.arrival for p in ps)
    last = max(s.end for s in segments)
    total = last - first
    if total <= 0:
        return 0.0
    busy = sum(s.end - s.start for s in segments)
    return busy / total * 100.0


def gantt(segments: list[Segment]) -> str:
    if not segments:
        return "(empty)"
    line = " | ".join(f"{s.name} [{s.start}-{s.end}]" for s in segments)
    return line


def parse_processes(spec: str) -> list[Process]:
    processes = []
    for item in spec.split(","):
        parts = item.strip().split(":")
        if len(parts) != 4:
            raise ValueError(
                f"invalid process '{item}'. Expected NAME:ARRIVAL:BURST:PRIORITY"
            )
        name, arrival, burst, prio = parts
        processes.append(Process(name, int(arrival), int(burst), int(prio)))
    return processes


DEMO_PROCESSES = [
    Process("P1", 0, 7, 2),
    Process("P2", 2, 4, 1),
    Process("P3", 4, 1, 3),
    Process("P4", 5, 4, 2),
]


def print_report(
    algorithm: str,
    processes: list[Process],
    results: list[Result],
    segments: list[Segment],
) -> None:
    print(f"\n=== {algorithm.upper()} SCHEDULING ===")
    print(f"{'PID':<7}{'AT':>5}{'BT':>5}{'PR':>5}{'CT':>5}{'TAT':>6}{'WT':>6}{'RT':>6}")
    print("-" * 45)
    for r in sorted(results, key=lambda x: x.name):
        print(
            f"{r.name:<7}{r.arrival:>5}{r.burst:>5}{r.priority:>5}"
            f"{r.completion:>5}{r.turnaround:>6}{r.waiting:>6}{r.response:>6}"
        )
    avg = averages(results)
    print("-" * 45)
    print(f"Average Waiting Time   : {avg['waiting']:.2f}")
    print(f"Average Turnaround     : {avg['turnaround']:.2f}")
    print(f"Average Response Time  : {avg['response']:.2f}")
    print(f"CPU Utilisation        : {cpu_utilisation(processes, segments):.2f}%")
    print(f"Gantt Chart             : {gantt(segments)}")


def demo_all() -> None:
    print("Workload: P1(AT=0,BT=7,PR=2), P2(2,4,1), P3(4,1,3), P4(5,4,2)")
    for name in ("fcfs", "sjf", "srtf", "priority", "rr"):
        results, segments = simulate(name, DEMO_PROCESSES, quantum=2)
        print_report(name, DEMO_PROCESSES, results, segments)
