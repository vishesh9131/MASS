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

if __name__ == "__main__":
    main()