"""Inter-process communication demonstrations."""

from __future__ import annotations

import multiprocessing as mp
import os
import time


def pipe_demo() -> None:
    print("\n=== IPC: PIPE ===")
    parent_conn, child_conn = mp.Pipe()

    def child(conn):
        message = conn.recv()
        print(f"[child] received: {message}", flush=True)
        conn.send(f"ACK from child PID {os.getpid()}")
        conn.close()

    process = mp.Process(target=child, args=(child_conn,), name="PipeChild")
    process.start()
    parent_conn.send("Hello from parent through a pipe")
    reply = parent_conn.recv()
    process.join()
    parent_conn.close()
    print(f"[parent] received: {reply}")


def queue_demo() -> None:
    print("\n=== IPC: MULTIPROCESSING QUEUE ===")
    queue = mp.Queue()

    def producer(q):
        for value in (10, 20, 30):
            q.put(value)
            print(f"[producer] sent {value}", flush=True)
        q.put(None)

    process = mp.Process(target=producer, args=(queue,), name="QueueProducer")
    process.start()

    total = 0
    while True:
        value = queue.get()
        if value is None:
            break
        total += value
        print(f"[parent] consumed {value}")

    process.join()
    print(f"Total consumed: {total}")


def shared_memory_demo() -> None:
    print("\n=== IPC: SHARED MEMORY VALUE ===")
    value = mp.Value("i", 0)

    def worker(shared):
        for _ in range(5):
            with shared.get_lock():
                shared.value += 1
            time.sleep(0.05)

    process = mp.Process(target=worker, args=(value,), name="SharedMemoryWorker")
    process.start()
    process.join()
    print(f"Shared value after child update: {value.value}")


def run_all() -> None:
    pipe_demo()
    queue_demo()
    shared_memory_demo()
