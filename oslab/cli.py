"""Command-line interface for the OS laboratory."""

from __future__ import annotations

import argparse
import os

from . import __version__
from .ipc_demo import run_all as run_ipc
from .process_tools import (
    create_process_demo,
    list_processes,
    print_process_info,
    process_management_demo,
    signal_demo,
)
from .scheduling import DEMO_PROCESSES, demo_all, parse_processes, print_report, simulate
from .system_info import print_system_snapshot, service_overview
from .thread_demo import race_condition_concept, run_thread_demo


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="oslab",
        description="Linux OS Services, Processes, Scheduling, Threads and IPC Lab",
    )
    parser.add_argument("--version", action="version", version=__version__)

    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("system", help="show Linux system information")
    sub.add_parser("services", help="inspect available Linux service tools")
    sub.add_parser("processes", help="show a read-only running process snapshot")

    pinfo = sub.add_parser("process-info", help="inspect one process")
    pinfo.add_argument("pid", type=int)

    proc = sub.add_parser("process", help="process creation and management demos")
    proc_sub = proc.add_subparsers(dest="process_command", required=True)
    proc_sub.add_parser("create", help="create and wait for a child process")
    proc_sub.add_parser("manage", help="demonstrate process lifecycle management")
    proc_sub.add_parser("signal", help="demonstrate signal-based IPC")

    sched = sub.add_parser("scheduling", help="CPU scheduling simulations")
    sched_sub = sched.add_subparsers(dest="scheduling_command", required=True)
    sched_sub.add_parser("demo", help="run all algorithms on the built-in workload")
    run = sched_sub.add_parser("run", help="run one scheduling algorithm")
    run.add_argument(
        "--algorithm",
        choices=["fcfs", "sjf", "srtf", "priority", "rr"],
        required=True,
    )
    run.add_argument("--quantum", type=int, default=2)
    run.add_argument(
        "--processes",
        default=None,
        help="NAME:ARRIVAL:BURST:PRIORITY, comma-separated",
    )

    threads = sub.add_parser("threads", help="run thread synchronization demo")
    threads.add_argument("--workers", type=int, default=4)
    threads.add_argument("--increments", type=int, default=1000)

    sub.add_parser("ipc", help="run pipe, queue and shared-memory demos")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "system":
        print_system_snapshot()
    elif args.command == "services":
        service_overview()
    elif args.command == "processes":
        list_processes()
    elif args.command == "process-info":
        if args.pid <= 0:
            raise SystemExit("PID must be positive")
        print_process_info(args.pid)
    elif args.command == "process":
        if args.process_command == "create":
            create_process_demo()
        elif args.process_command == "manage":
            process_management_demo()
        elif args.process_command == "signal":
            signal_demo()
    elif args.command == "scheduling":
        if args.scheduling_command == "demo":
            demo_all()
        else:
            processes = (
                parse_processes(args.processes)
                if args.processes
                else DEMO_PROCESSES
            )
            results, segments = simulate(args.algorithm, processes, args.quantum)
            print_report(args.algorithm, processes, results, segments)
    elif args.command == "threads":
        if args.workers <= 0 or args.increments <= 0:
            raise SystemExit("workers and increments must be positive")
        run_thread_demo(args.workers, args.increments)
        race_condition_concept()
    elif args.command == "ipc":
        run_ipc()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
