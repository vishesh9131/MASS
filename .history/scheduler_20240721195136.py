import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configuration
WORKER_NODES = ['http://correct_ip_1/api/metrics', 'http://correct_ip_2/api/metrics']
RULES = [
    {'expression': 'metric1 > 80', 'alert': 'High metric1 value'},
    {'expression': 'metric2 < 20', 'alert': 'Low metric2 value'}
]

def collect_metrics():
    metrics = {}
    for node in WORKER_NODES:
        try:
            response = requests.get(node)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            metrics[node] = response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to collect metrics from {node}: {e}")
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
        # Example task assignment logic
        task = {"task": "example_task", "node": node}
        send_task_to_node(task)

def trigger_alerts(results):
    for node, alert in results:
        logging.warning(f"Alert triggered for {node}: {alert}")
        # Example alert triggering logic
        alert_message = {"alert": alert, "node": node}
        send_alert(alert_message)

def display_results(results):
    for node, alert in results:
        logging.info(f"Node: {node}, Alert: {alert}")