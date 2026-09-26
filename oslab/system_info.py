"""Linux system and service inspection utilities."""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
from pathlib import Path


def _read(path: str) -> str:
    try:
        return Path(path).read_text(errors="replace").strip()
    except (OSError, PermissionError):
        return "Unavailable"


def system_snapshot() -> dict[str, str]:
    meminfo = _read("/proc/meminfo")
    mem_total = "Unavailable"
    mem_available = "Unavailable"
    for line in meminfo.splitlines():
        if line.startswith("MemTotal:"):
            mem_total = line.split(":", 1)[1].strip()
        elif line.startswith("MemAvailable:"):
            mem_available = line.split(":", 1)[1].strip()

    uptime = _read("/proc/uptime")
    uptime_seconds = uptime.split()[0] if uptime else "Unavailable"

    return {
        "OS": platform.platform(),
        "Kernel": platform.release(),
        "Architecture": platform.machine(),
        "Hostname": platform.node(),
        "Python": platform.python_version(),
        "CPU cores (logical)": str(os.cpu_count() or "Unavailable"),
        "Memory total": mem_total,
        "Memory available": mem_available,
        "Uptime (seconds)": uptime_seconds,
    }


def print_system_snapshot() -> None:
    print("\n=== LINUX SYSTEM INFORMATION ===")
    for key, value in system_snapshot().items():
        print(f"{key:<24}: {value}")


def available_service_tools() -> list[tuple[str, str]]:
    commands = [
        ("systemctl", "systemctl --version"),
        ("service", "service --status-all"),
        ("journalctl", "journalctl --version"),
    ]
    result = []
    for name, command in commands:
        result.append((name, "available" if shutil.which(name) else "not installed"))
    return result


def service_overview() -> None:
    print("\n=== LINUX SERVICE MANAGEMENT TOOLS ===")
    for name, status in available_service_tools():
        print(f"{name:<14}: {status}")
    print("\nNo service is modified by this program.")
    print("Useful commands on systemd systems:")
    print("  systemctl list-units --type=service")
    print("  systemctl --failed")
    print("  systemctl status <service>")
    print("  journalctl -u <service>")


def command_output(command: list[str]) -> str:
    try:
        completed = subprocess.run(
            command, capture_output=True, text=True, timeout=5, check=False
        )
        return (completed.stdout or completed.stderr).strip()
    except (OSError, subprocess.SubprocessError):
        return "Command unavailable."
