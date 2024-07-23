import time
from scheduler import collect_metrics, evaluate_rules, display_results, assign_tasks, trigger_alerts

from scheduler import worker_nodes_api

worker_nodes_api = ['http://localhost:8000/api/metrics', 'http://localhost:8001/api/metrics']



INTERVAL = 60 

def main():
    while True:
        metrics = collect_metrics()
        results = evaluate_rules(metrics)
        display_results(results)
        assign_tasks(results)
        trigger_alerts(results)
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()