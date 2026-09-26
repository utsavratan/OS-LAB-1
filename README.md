# OPERATING SYSTEMS — LINUX PRACTICAL LAB

<div align="center">

# Linux OS Services, Processes, Scheduling, Threads & IPC Lab

### Python + Linux Based Operating Systems Practical Project

**Utsav Ratan**  
**Enrollment No.: 2401010046**  
**Programme: B.Tech CSE Core**  
**Section: B**  
**Subject: Operating Systems**

</div>

---

## 1. Project Overview

This project is a **complete Python + Linux based Operating Systems practical laboratory** designed to demonstrate and understand fundamental OS concepts through executable programs.

The project covers:

- Linux operating-system services and system information
- Process creation and process lifecycle management
- Process observation using Linux `/proc` and `ps`
- CPU scheduling simulation
- FCFS scheduling
- SJF scheduling
- SRTF scheduling
- Priority scheduling
- Round Robin scheduling
- Scheduling performance analysis
- Waiting time, turnaround time and response time
- CPU utilisation
- Gantt chart generation
- Python threads
- Thread synchronization using locks
- Inter-process communication (IPC)
- Pipes
- Multiprocessing queues
- Shared memory
- Unix signals
- Automated unit testing
- Reproducible command-line demonstrations

The implementation uses the **Python standard library only**, making the project lightweight, portable and easy to run on Linux systems.

---

# 2. Learning Objectives

After completing this practical, a student should be able to:

1. Understand basic Linux OS services and system information.
2. Observe active Linux processes.
3. Understand parent and child processes.
4. Create and manage processes using Python.
5. Understand process lifecycle operations such as `start()` and `join()`.
6. Understand CPU scheduling and scheduling queues.
7. Implement major CPU scheduling algorithms.
8. Calculate scheduling performance metrics.
9. Construct and interpret Gantt charts.
10. Understand the difference between processes and threads.
11. Synchronize threads accessing shared data.
12. Understand inter-process communication.
13. Demonstrate IPC using pipes, queues and shared memory.
14. Understand basic signal-based communication.
15. Run and validate OS experiments from the Linux terminal.

---

# 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.10+ | Program implementation |
| Linux / Ubuntu | Operating-system environment |
| `/proc` | Process observation |
| `ps` | Process monitoring |
| `systemctl` | Linux service inspection |
| `multiprocessing` | Process creation and IPC |
| `threading` | Thread programming |
| `signal` | Signal-based IPC |
| `unittest` | Automated testing |
| Bash | Linux launcher |

### Dependencies

**No third-party Python packages are required.**

The project uses only the Python standard library.

---

# 4. System Requirements

### Minimum Requirements

- Linux / Ubuntu
- Ubuntu 20.04+ recommended
- Python 3.10 or newer
- Terminal access
- Standard Linux utilities

### WSL2

The project can also be used with **WSL2**.

Some service-management functionality may differ from a full Ubuntu installation because WSL configurations do not always run `systemd`.

---

# 5. Verify Your Environment

Open a Linux terminal and run:

```bash
python3 --version
uname -a
```

You can also verify the Python installation:

```bash
python3 -c "import sys; print(sys.version)"
```

---

# 6. Project Structure

```text
os_process_scheduling_lab/
│
├── README.md
├── LICENSE
├── requirements.txt
├── run.py
├── .gitignore
│
├── oslab/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   │
│   ├── system_info.py
│   ├── process_tools.py
│   ├── scheduling.py
│   ├── thread_demo.py
│   └── ipc_demo.py
│
├── scripts/
│   └── oslab
│
└── tests/
    ├── test_process_tools.py
    └── test_scheduling.py
```

### Module Description

| File | Responsibility |
|---|---|
| `cli.py` | Main command-line interface |
| `system_info.py` | Linux system and service information |
| `process_tools.py` | Process observation, creation, management and signals |
| `scheduling.py` | CPU scheduling algorithms and metrics |
| `thread_demo.py` | Thread and synchronization demonstration |
| `ipc_demo.py` | IPC demonstrations |
| `test_process_tools.py` | Process-related tests |
| `test_scheduling.py` | Scheduling algorithm tests |
| `scripts/oslab` | Linux launcher |

---

# 7. Installation / Setup

Extract the project ZIP and enter the project directory:

```bash
cd os_process_scheduling_lab
```

Optional: create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

No package installation is required.

You can verify the project immediately:

```bash
python3 -m oslab --help
```

---

# 8. Command-Line Interface

The complete project is controlled through one CLI:

```bash
python3 -m oslab --help
```

Available commands:

```text
system
services
processes
process-info
process
scheduling
threads
ipc
```

A Linux launcher is also included:

```bash
./scripts/oslab --help
```

---

# 9. Experiment 1 — Linux System Information

## Objective

To observe basic information about the Linux operating system and the machine on which the program is executing.

## Run

```bash
python3 -m oslab system
```

## Information Displayed

The program reports:

- Operating system
- Kernel version
- Architecture
- Hostname
- Python version
- Logical CPU count
- Total memory
- Available memory
- System uptime

### Linux Concepts Demonstrated

- Kernel
- CPU resources
- Memory resources
- `/proc`
- Operating-system information interfaces

---

# 10. Experiment 2 — Linux OS Services

## Objective

To understand Linux service-management facilities and identify service-management utilities available on the system.

## Run

```bash
python3 -m oslab services
```

The program checks for common tools such as:

```text
systemctl
service
journalctl
```

### Useful Linux Commands

```bash
systemctl list-units --type=service
```

```bash
systemctl --failed
```

```bash
systemctl status <service>
```

```bash
journalctl -u <service>
```

> **Safety:** The project only inspects service-management capabilities. It does not start, stop, restart or modify system services.

---

# 11. Experiment 3 — Process Observation

## Objective

To observe running Linux processes and understand the information maintained by the operating system for each process.

## Run

```bash
python3 -m oslab processes
```

The program displays a read-only process snapshot using Linux `ps`.

Typical information includes:

```text
PID
PPID
STATE
CPU %
MEMORY %
ELAPSED TIME
COMMAND
```

---

## Inspect a Specific Process

Run:

```bash
python3 -m oslab process-info $$
```

Here `$$` represents the PID of the current shell.

The program reads information from:

```text
/proc/<PID>/
```

and displays information such as:

- PID
- Process name
- Process state
- Parent PID
- Number of threads
- Resident memory
- Command line

---

## Manual `/proc` Observation

Linux also allows direct inspection:

```bash
cat /proc/$$/status
```

```bash
cat /proc/$$/cmdline
```

```bash
ls -l /proc/$$/fd
```

### Important Concept

`/proc` is a **pseudo-filesystem** provided by the Linux kernel. It exposes runtime information about processes and other kernel-managed resources.

---

# 12. Experiment 4 — Process Creation

## Objective

To understand process creation and the relationship between a parent process and a child process.

## Run

```bash
python3 -m oslab process create
```

### Demonstration

The parent process:

1. Starts.
2. Creates a child process.
3. Receives the child's PID.
4. Waits for the child.
5. Reads the child's exit status.

The child process:

1. Starts.
2. Displays its PID and parent PID.
3. Performs simulated work.
4. Exits normally.

### Concepts Demonstrated

- Process ID
- Parent Process ID
- Child process
- Process creation
- `start()`
- `join()`
- Exit status

---

# 13. Experiment 5 — Process Management

## Objective

To understand process lifecycle management.

## Run

```bash
python3 -m oslab process manage
```

The experiment demonstrates:

```text
Parent
  │
  ├── start()
  │
  ▼
Child / Worker
  │
  ├── execute
  │
  └── exit
  │
  ▼
Parent
  │
  └── join()
```

### Concepts Demonstrated

- Process lifecycle
- Process state
- Synchronization between parent and child
- `is_alive()`
- `join()`
- Exit codes

---

# 14. Experiment 6 — Signal-Based Communication

## Objective

To demonstrate how a process can receive a Unix signal from another process.

## Run

```bash
python3 -m oslab process signal
```

The demonstration uses:

```text
SIGUSR1
```

The parent sends the signal and the child installs a signal handler.

### Concept

Signals provide a lightweight asynchronous notification mechanism between processes.

---

# 15. Experiment 7 — CPU Scheduling

## Objective

To implement and compare major CPU scheduling algorithms.

The simulator supports:

1. FCFS
2. SJF
3. SRTF
4. Priority
5. Round Robin

The scheduler is a **discrete-event simulator**. It does not actually sleep for the simulated CPU burst times, so large experiments execute quickly.

---

# 16. Scheduling Input Format

Each process is represented as:

```text
NAME:ARRIVAL_TIME:BURST_TIME:PRIORITY
```

Example:

```text
P1:0:5:2
```

means:

```text
Process       P1
Arrival       0
Burst         5
Priority      2
```

Multiple processes are comma-separated:

```text
P1:0:5:2,P2:1:3:1,P3:2:4:3
```

### Priority Rule

A **smaller priority number means higher priority**.

---

# 17. Experiment 7A — FCFS

## First Come, First Served

FCFS executes processes in the order in which they become ready.

## Run

```bash
python3 -m oslab scheduling run --algorithm fcfs
```

### Concept

```text
Ready Queue

P1 → P2 → P3 → P4
```

The first eligible process receives the CPU and normally runs until completion.

---

# 18. Experiment 7B — SJF

## Shortest Job First

SJF selects the available process with the shortest CPU burst.

## Run

```bash
python3 -m oslab scheduling run --algorithm sjf
```

### Concept

```text
Select process with minimum burst time
```

SJF in this project is **non-preemptive**.

---

# 19. Experiment 7C — SRTF

## Shortest Remaining Time First

SRTF is the preemptive version of shortest-job scheduling.

## Run

```bash
python3 -m oslab scheduling run --algorithm srtf
```

### Concept

At each scheduling decision, the process with the smallest remaining CPU time is selected.

A running process can therefore be preempted when a new process with a shorter remaining time arrives.

---

# 20. Experiment 7D — Priority Scheduling

## Run

```bash
python3 -m oslab scheduling run --algorithm priority
```

The process with the highest priority is selected.

In this implementation:

```text
Priority 1 → higher priority than Priority 2
Priority 2 → higher priority than Priority 3
```

The implementation is non-preemptive.

---

# 21. Experiment 7E — Round Robin

## Run

```bash
python3 -m oslab scheduling run --algorithm rr --quantum 2
```

The **time quantum** determines how long a process can execute before returning to the ready queue.

Example:

```text
Quantum = 2
```

A process with burst time `7` can execute in approximately:

```text
2 + 2 + 2 + 1
```

depending on the ready queue and arrivals.

---

# 22. Custom Scheduling Workload

Run:

```bash
python3 -m oslab scheduling run \
  --algorithm rr \
  --quantum 3 \
  --processes "P1:0:5:2,P2:1:3:1,P3:2:4:3"
```

The same workload can be tested with different algorithms:

```bash
python3 -m oslab scheduling run \
  --algorithm fcfs \
  --processes "P1:0:5:2,P2:1:3:1,P3:2:4:3"
```

```bash
python3 -m oslab scheduling run \
  --algorithm sjf \
  --processes "P1:0:5:2,P2:1:3:1,P3:2:4:3"
```

```bash
python3 -m oslab scheduling run \
  --algorithm srtf \
  --processes "P1:0:5:2,P2:1:3:1,P3:2:4:3"
```

```bash
python3 -m oslab scheduling run \
  --algorithm priority \
  --processes "P1:0:5:2,P2:1:3:1,P3:2:4:3"
```

---

# 23. Scheduling Performance Metrics

For every process, the simulator calculates:

| Metric | Formula |
|---|---|
| Completion Time | Time at which process finishes |
| Turnaround Time | `CT - AT` |
| Waiting Time | `TAT - BT` |
| Response Time | `First Start - AT` |

Where:

```text
AT = Arrival Time
BT = Burst Time
CT = Completion Time
TAT = Turnaround Time
WT = Waiting Time
RT = Response Time
```

---

## Turnaround Time

```text
Turnaround Time = Completion Time - Arrival Time
```

---

## Waiting Time

```text
Waiting Time = Turnaround Time - Burst Time
```

---

## Response Time

```text
Response Time = First Start Time - Arrival Time
```

---

## CPU Utilisation

```text
CPU Utilisation =
Busy CPU Time / Total Elapsed Scheduling Time × 100
```

---

# 24. Gantt Chart

Every scheduling experiment generates a compact Gantt representation.

Example:

```text
P1 [0-2] | P2 [2-4] | P1 [4-6] | P3 [6-7]
```

This makes CPU allocation and preemption easy to observe.

---

# 25. Run All Scheduling Algorithms

For the complete built-in workload:

```bash
python3 -m oslab scheduling demo
```

The demonstration compares:

```text
FCFS
SJF
SRTF
Priority
Round Robin
```

For each algorithm, the program reports:

- Per-process metrics
- Average waiting time
- Average turnaround time
- Average response time
- CPU utilisation
- Gantt chart

---

# 26. Built-in Scheduling Workload

The default workload is:

| Process | Arrival | Burst | Priority |
|---|---:|---:|---:|
| P1 | 0 | 7 | 2 |
| P2 | 2 | 4 | 1 |
| P3 | 4 | 1 | 3 |
| P4 | 5 | 4 | 2 |

This same workload can be used to observe how the scheduling policy changes CPU allocation and performance metrics.

---

# 27. Experiment 8 — Threads & Synchronization

## Objective

To understand threads, shared memory and synchronization.

## Run

```bash
python3 -m oslab threads
```

The program creates multiple worker threads that update a shared counter.

A:

```python
threading.Lock()
```

is used to protect the shared state.

### Default Configuration

```text
Workers     = 4
Increments  = 1000 per worker
Expected    = 4000
```

The final result is checked automatically.

---

## Custom Thread Experiment

Example:

```bash
python3 -m oslab threads --workers 8 --increments 5000
```

### Concepts Demonstrated

- Thread creation
- Concurrent execution
- Shared memory
- Critical section
- Mutual exclusion
- Locking
- `start()`
- `join()`

---

# 28. Thread Synchronization

The shared counter represents a critical section.

Conceptually:

```text
Thread 1 ─┐
Thread 2 ─┤
Thread 3 ─┼──> Shared Counter
Thread 4 ─┘
             │
             ▼
          Lock
```

The lock ensures that only one thread modifies the shared counter at a time.

---

# 29. Experiment 9 — Inter-Process Communication

## Objective

To demonstrate mechanisms through which independent processes exchange data or coordinate execution.

## Run

```bash
python3 -m oslab ipc
```

The program demonstrates:

1. Pipe communication
2. Multiprocessing Queue
3. Shared memory

The project also includes a separate signal-based process communication experiment.

---

# 30. IPC — Pipe

A parent and child process communicate using a pipe.

Conceptually:

```text
Parent
   │
   │ message
   ▼
 PIPE
   │
   ▼
Child
   │
   │ reply
   ▼
Parent
```

Run:

```bash
python3 -m oslab ipc
```

---

# 31. IPC — Multiprocessing Queue

A producer process places values into a multiprocessing queue.

The parent consumes the values.

Example flow:

```text
Producer
   │
   ├── 10
   ├── 20
   └── 30
        │
        ▼
      Queue
        │
        ▼
     Consumer
```

The program calculates the total consumed value.

---

# 32. IPC — Shared Memory

The project demonstrates shared state using:

```python
multiprocessing.Value
```

A child process modifies a shared integer while using synchronization.

This demonstrates the basic idea of **shared-memory IPC**.

---

# 33. IPC — Signals

Signals provide another form of process communication.

Run:

```bash
python3 -m oslab process signal
```

The parent sends:

```text
SIGUSR1
```

and the child handles the signal.

---

# 34. Automated Testing

The project includes automated tests for core functionality.

Run:

```bash
python3 -m unittest discover -v
```

The test suite checks:

- FCFS scheduling calculations
- Round Robin completion
- Scheduling metric validity
- Invalid quantum handling
- Duplicate process validation
- Linux process inspection

A successful run should report all tests as passing.

---

# 35. Complete Practical Demonstration

For a complete classroom demonstration, run the following sequence:

### Step 1 — System

```bash
python3 -m oslab system
```

### Step 2 — Services

```bash
python3 -m oslab services
```

### Step 3 — Processes

```bash
python3 -m oslab processes
```

### Step 4 — Current Process

```bash
python3 -m oslab process-info $$
```

### Step 5 — Process Creation

```bash
python3 -m oslab process create
```

### Step 6 — Process Management

```bash
python3 -m oslab process manage
```

### Step 7 — Signals

```bash
python3 -m oslab process signal
```

### Step 8 — Scheduling

```bash
python3 -m oslab scheduling demo
```

### Step 9 — Threads

```bash
python3 -m oslab threads
```

### Step 10 — IPC

```bash
python3 -m oslab ipc
```

### Step 11 — Tests

```bash
python3 -m unittest discover -v
```

---

# 36. Expected Learning Outcomes

After executing the project, the following relationships should be clear:

```text
Linux
 │
 ├── Processes
 │     ├── PID
 │     ├── PPID
 │     ├── State
 │     └── Resources
 │
 ├── CPU Scheduling
 │     ├── FCFS
 │     ├── SJF
 │     ├── SRTF
 │     ├── Priority
 │     └── Round Robin
 │
 ├── Threads
 │     └── Synchronization
 │
 └── IPC
       ├── Pipes
       ├── Queues
       ├── Shared Memory
       └── Signals
```

---

# 37. Important Linux Commands for Viva / Practical

### Process list

```bash
ps
```

```bash
ps aux
```

### Process tree

```bash
pstree
```

### Current process ID

```bash
echo $$
```

### Process information

```bash
cat /proc/<PID>/status
```

### Command line

```bash
cat /proc/<PID>/cmdline
```

### Open file descriptors

```bash
ls -l /proc/<PID>/fd
```

### System information

```bash
uname -a
```

### Memory

```bash
free -h
```

### CPU information

```bash
lscpu
```

### Services

```bash
systemctl list-units --type=service
```

---

# 38. Important Viva Questions

### Q1. What is a process?

A process is a program in execution with its own execution state and operating-system-managed resources.

### Q2. What is a PID?

PID stands for Process ID. It uniquely identifies a process within the operating system's process namespace.

### Q3. What is a PPID?

PPID stands for Parent Process ID and identifies the process that created or is responsible for the child process.

### Q4. What is a thread?

A thread is an execution unit within a process. Threads of the same process generally share its address space and resources.

### Q5. What is IPC?

IPC stands for Inter-Process Communication. It provides mechanisms through which processes exchange data or coordinate execution.

### Q6. What is FCFS?

First Come, First Served schedules processes according to their arrival order.

### Q7. What is SJF?

Shortest Job First selects the available process with the smallest CPU burst.

### Q8. What is SRTF?

Shortest Remaining Time First is the preemptive form of shortest-job scheduling.

### Q9. What is Round Robin?

Round Robin gives each ready process a fixed time quantum in cyclic order.

### Q10. What is a critical section?

A critical section is a portion of code that accesses shared resources and must be protected against unsafe concurrent access.

### Q11. Why is a lock used?

A lock provides mutual exclusion so that concurrent threads do not simultaneously modify protected shared state.

### Q12. What is `/proc`?

`/proc` is a Linux pseudo-filesystem exposing information about processes and kernel-managed system resources.

---

# 39. Safety & Design

This project is intentionally designed to be safe for educational use.

It:

- Does not require root privileges.
- Does not terminate arbitrary system processes.
- Does not change process priorities.
- Does not modify CPU scheduling policy.
- Does not start or stop system services.
- Uses read-only process inspection where possible.
- Uses simulated CPU workloads instead of consuming CPU for long periods.
- Uses controlled child processes for demonstrations.

---

# 40. Code Quality

The project follows a modular structure:

```text
CLI
 │
 ├── System Information
 │
 ├── Process Management
 │
 ├── Scheduling Engine
 │
 ├── Thread Demonstration
 │
 └── IPC Demonstrations
```

Core scheduling logic is separated from the command-line interface, allowing the algorithms to be tested independently.

Input validation is included for:

- Empty process lists
- Duplicate process names
- Invalid burst times
- Invalid arrival times
- Invalid Round Robin quantum
- Invalid process specification

---

# 41. Quick Reference

| Task | Command |
|---|---|
| Help | `python3 -m oslab --help` |
| System info | `python3 -m oslab system` |
| Services | `python3 -m oslab services` |
| Processes | `python3 -m oslab processes` |
| Process info | `python3 -m oslab process-info <PID>` |
| Create process | `python3 -m oslab process create` |
| Manage process | `python3 -m oslab process manage` |
| Signals | `python3 -m oslab process signal` |
| Scheduling demo | `python3 -m oslab scheduling demo` |
| FCFS | `python3 -m oslab scheduling run --algorithm fcfs` |
| SJF | `python3 -m oslab scheduling run --algorithm sjf` |
| SRTF | `python3 -m oslab scheduling run --algorithm srtf` |
| Priority | `python3 -m oslab scheduling run --algorithm priority` |
| Round Robin | `python3 -m oslab scheduling run --algorithm rr --quantum 2` |
| Threads | `python3 -m oslab threads` |
| IPC | `python3 -m oslab ipc` |
| Tests | `python3 -m unittest discover -v` |

---

# 42. Submission Checklist

Before submitting the practical, verify:

- [ ] Python version verified
- [ ] Linux environment verified
- [ ] System information demonstrated
- [ ] Linux services inspected
- [ ] Processes observed
- [ ] `/proc` inspected
- [ ] Process creation demonstrated
- [ ] Process management demonstrated
- [ ] Signal communication demonstrated
- [ ] FCFS executed
- [ ] SJF executed
- [ ] SRTF executed
- [ ] Priority executed
- [ ] Round Robin executed
- [ ] Scheduling metrics observed
- [ ] Gantt charts observed
- [ ] Threads demonstrated
- [ ] Synchronization demonstrated
- [ ] Pipe IPC demonstrated
- [ ] Queue IPC demonstrated
- [ ] Shared memory demonstrated
- [ ] Automated tests passed

---

# 43. Final Conclusion

This practical project provides a complete hands-on demonstration of fundamental Operating Systems concepts using Python and Linux.

It connects theoretical concepts with executable experiments:

```text
OS Services
     ↓
Processes
     ↓
Process Management
     ↓
CPU Scheduling
     ↓
Threads & Synchronization
     ↓
Inter-Process Communication
```

The project can therefore be used for:

- Operating Systems laboratory work
- Classroom demonstrations
- Practical examinations
- Viva preparation
- Scheduling experiments
- Linux process-management experiments
- Python multiprocessing and threading practice

---

<div align="center">

## OPERATING SYSTEMS PRACTICAL

**Utsav Ratan — 2401010046**  
**B.Tech CSE Core — Section B**

### Linux OS Services, Processes, Scheduling, Threads & IPC Lab

</div>
