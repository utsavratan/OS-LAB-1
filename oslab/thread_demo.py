"""Threading demonstrations."""

from __future__ import annotations

import threading
import time


def run_thread_demo(workers: int = 4, increments: int = 1000) -> int:
    """Increment shared state safely using a Lock."""
    counter = {"value": 0}
    lock = threading.Lock()

    def worker(worker_id: int) -> None:
        local = 0
        for _ in range(increments):
            local += 1
            with lock:
                counter["value"] += 1
        print(f"[thread {worker_id}] completed {local} increments", flush=True)

    threads = [
        threading.Thread(target=worker, args=(i,), name=f"Worker-{i}")
        for i in range(1, workers + 1)
    ]

    print("\n=== THREADS & SYNCHRONIZATION DEMO ===")
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    expected = workers * increments
    print(f"Expected counter : {expected}")
    print(f"Actual counter   : {counter['value']}")
    print(f"Result           : {'PASS' if counter['value'] == expected else 'FAIL'}")
    return counter["value"]


def race_condition_concept() -> None:
    print("\nConcept:")
    print("- Threads share the same process memory.")
    print("- A Lock prevents two threads from updating shared state simultaneously.")
    print("- Without synchronization, read-modify-write operations can race.")
