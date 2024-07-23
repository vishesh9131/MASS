# MASS - Memory Aware Scheduling System

## Abstract

Mass consists of a memory allocator written in C and a scheduler written in Python. The memory allocator provides a simple memory pool for dynamic memory allocation, while the scheduler collects metrics from worker nodes, evaluates rules, assigns tasks, triggers alerts, and allocates memory based on the collected metrics.

## Memory Allocator

The memory allocator is implemented in C and provides functions to allocate, reallocate, and free memory from a fixed-size memory pool. It uses a mutex to ensure thread safety.

### Key Functions

- **allocate_memory(size_t size)**: Allocates memory of the specified size from the memory pool.
- **reallocate_memory(void* ptr, size_t new_size)**: Reallocates memory to a new size, copying the old data to the new location.
- **free_memory(void* ptr)**: A no-op in this simple memory pool implementation.
- **reset_memory_pool()**: Resets the memory pool, making all memory available again.



---
# Scheduler

The scheduler is implemented in Python and performs the following tasks:

1. **Collect Metrics**: Collects metrics from worker nodes.
2. **Evaluate Rules**: Evaluates predefined rules against the collected metrics.
3. **Assign Tasks**: Assigns tasks to nodes based on the evaluation results.
4. **Trigger Alerts**: Triggers alerts based on the evaluation results.
5. **Allocate Memory**: Allocates memory based on the collected metrics using the C memory allocator.

### Key Functions

- **collect_metrics()**: Collects metrics from worker nodes.
- **evaluate_rules(metrics)**: Evaluates rules against the collected metrics.
- **assign_tasks(results)**: Assigns tasks to nodes based on the evaluation results.
- **trigger_alerts(results)**: Triggers alerts based on the evaluation results.
- **allocate_memory(metrics)**: Allocates memory based on the collected metrics.


---
# Running the Project

### Prerequisites

- Python 3.x
- GCC (for compiling the C code)
- `requests` library for Python

### Steps

1. **Compile the Memory Allocator**

   ```sh
   gcc -shared -o memory_allocator.so -fPIC memory_allocator.c -lpthread
   ```

2. **Run the Scheduler**

   ```sh
   python main.py
   ```

### Code Reference
```python
import time
from scheduler import collect_metrics, evaluate_rules, display_results, assign_tasks, trigger_alerts, allocate_memory

INTERVAL = 6

def main():
    while True:
        metrics = collect_metrics()
        results = evaluate_rules(metrics)
        display_results(results)
        assign_tasks(results)
        trigger_alerts(results)
        allocate_memory(metrics)
        time.sleep(INTERVAL)
if name == "main":
    main()
```


## Rules Configuration

The rules for evaluating metrics are defined in `rules.py`. You can modify these rules to fit your requirements.

### scheduler/RULES.py
 
```python
RULES = [
{'expression': 'metric1 > 80', 'alert': 'High metric1 value'},
{'expression': 'metric2 < 20', 'alert': 'Low metric2 value'},
{'expression': 'metric3 > 100', 'alert': 'High metric3 value'},
{'expression': 'metric4 < 50', 'alert': 'Low metric4 value'},
```

# Note
### 1.  Right now its in phase 1 of development. 
### 2. its not ready for 3rd-party production use. 
### 3. Its only for internal use at the moment for specific tech. 

>**Ready for revisions**

# **Cheers!**
