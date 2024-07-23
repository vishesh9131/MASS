import requests
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configuration
WORKER_NODES = ['http://worker1/api/metrics', 'http://worker2/api/metrics']
INTERVAL = 60  # Interval in seconds
RULES = [
    {'expression': 'metric1 > 80', 'alert': 'High metric1 value'},
    {'expression': 'metric2 < 20', 'alert': 'Low metric2 value'}
]

def collect_metrics():
    metrics = {}
    for node in WORKER_NODES:
        response = requests.get(node)
        if response.status_code == 200:
            metrics[node] = response.json()
        else:
            logging.error(f"Failed to collect metrics from {node}")
    return metrics

def evaluate_rules(metrics):
    results = []
    for rule in RULES:
        for node, node_metrics in metrics.items():
            if eval(rule['expression'], {}, node_metrics):
                results.append((node, rule['alert']))
    return results

def assign_tasks(results):
    for node, alert in results:
        logging.info(f"Assigning task to {node} due to {alert}")
        # Add task assignment logic here

def trigger_alerts(results):
    for node, alert in results:
        logging.warning(f"Alert triggered for {node}: {alert}")
        # Add alert triggering logic here

def main():
    while True:
        metrics = collect_metrics()
        results = evaluate_rules(metrics)
        display_results(results)
        assign_tasks(results)
        trigger_alerts(results)
        time.sleep(INTERVAL)

def display_results(results):
    for node, alert in results:
        logging.info(f"Node: {node}, Alert: {alert}")

if __name__ == "__main__":
    main()