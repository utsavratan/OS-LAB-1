"""Linux process creation, observation and management demonstrations."""

from __future__ import annotations

import multiprocessing as mp
import os
import signal
import subprocess
import time
from pathlib import Path


def _proc_value(pid: int, filename: str) -> str:
    path = Path(f"/proc/{pid}/{filename}")
    try:
        return path.read_text(errors="replace").strip()
    except (OSError, PermissionError):
        return "Unavailable"


def process_info(pid: int) -> dict[str, str]:
    """Return safe, read-only information for a Linux process."""
    status = _proc_value(pid, "status")
    values: dict[str, str] = {
        "PID": str(pid),
        "Status": "Unavailable",
        "Name": "Unavailable",
        "State": "Unavailable",
        "PPID": "Unavailable",
        "Threads": "Unavailable",
        "VmRSS": "Unavailable",
        "Command": "Unavailable",
    }
    if status != "Unavailable":
        for line in status.splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            value = value.strip()
            if key == "Name":
                values["Name"] = value
            elif key == "State":
                values["State"] = value
            elif key == "PPid":
                values["PPID"] = value
            elif key == "Threads":
                values["Threads"] = value
            elif key == "VmRSS":
                values["VmRSS"] = value
        values["Status"] = "Present"

    cmdline = _proc_value(pid, "cmdline")
    if cmdline != "Unavailable":
        values["Command"] = " ".join(part for part in cmdline.split("\x00") if part)

    return values


def print_process_info(pid: int) -> None:
    print(f"\n=== PROCESS {pid} ===")
    info = process_info(pid)
    for key, value in info.items():
        print(f"{key:<10}: {value}")

    try:
        result = subprocess.run(
            ["ps", "-p", str(pid), "-o", "pid,ppid,stat,%cpu,%mem,etime,cmd"],
            capture_output=True,
            text=True,
            check=False,
            timeout=3,
        )
        if result.stdout.strip():
            print("\n--- ps snapshot ---")
            print(result.stdout.rstrip())
    except (OSError, subprocess.SubprocessError):
        pass


def list_processes(limit: int = 15) -> None:
    print("\n=== RUNNING PROCESS SNAPSHOT ===")
    try:
        result = subprocess.run(
            ["ps", "-eo", "pid,ppid,stat,%cpu,%mem,comm", "--sort=-%cpu"],
            capture_output=True,
            text=True,
            check=False,
            timeout=3,
        )
        lines = result.stdout.strip().splitlines()
        if lines:
            print(lines[0])
            print("\n".join(lines[1 : limit + 1]))
            return
    except (OSError, subprocess.SubprocessError):
        pass

    print("ps is unavailable; showing /proc PIDs.")
    pids = sorted(
        int(p.name)
        for p in Path("/proc").iterdir()
        if p.name.isdigit()
    )
    print("PID")
    for pid in pids[:limit]:
        print(pid)


def _child_work() -> None:
    print(f"[child] PID={os.getpid()} PPID={os.getppid()}", flush=True)
    for step in range(1, 4):
        print(f"[child] working... step {step}/3", flush=True)
        time.sleep(0.25)
    print("[child] exiting with status 0", flush=True)


def create_process_demo() -> None:
    print("\n=== PROCESS CREATION DEMO ===")
    print(f"[parent] PID={os.getpid()}")
    process = mp.Process(target=_child_work, name="OSLabChild")
    process.start()
    print(f"[parent] created child PID={process.pid}")
    process.join()
    print(f"[parent] child exit code={process.exitcode}")


def _managed_worker() -> None:
    print(f"[worker] PID={os.getpid()} started", flush=True)
    time.sleep(0.6)
    print("[worker] completed gracefully", flush=True)


def process_management_demo() -> None:
    print("\n=== PROCESS MANAGEMENT DEMO ===")
    process = mp.Process(target=_managed_worker, name="ManagedWorker")
    process.start()
    print(f"[parent] started {process.name}, PID={process.pid}")
    print(f"[parent] alive={process.is_alive()}")
    process.join(timeout=2)
    print(f"[parent] alive after join={process.is_alive()}")
    print(f"[parent] exit code={process.exitcode}")


def signal_demo() -> None:
    """A small signal demonstration using a child process."""
    print("\n=== SIGNAL IPC DEMO ===")

    def worker(event: mp.Event) -> None:
        def handler(signum, _frame):
            print(f"[child] received signal {signum}", flush=True)
            event.set()

        signal.signal(signal.SIGUSR1, handler)
        print(f"[child] waiting for SIGUSR1; PID={os.getpid()}", flush=True)
        event.wait(3)

    event = mp.Event()
    child = mp.Process(target=worker, args=(event,), name="SignalWorker")
    child.start()
    time.sleep(0.2)
    os.kill(child.pid, signal.SIGUSR1)
    child.join(2)
    print(f"[parent] signal delivered; child exit code={child.exitcode}")
