import requests
import logging
from rules import RULES
# Configure logging
logging.basicConfig(level=logging.INFO)

# Configuration
WORKER_NODES = ['http://localhost:8000/api/metrics', 'http://localhost:8001/api/metrics']



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
        send_task_to_node(node, task)

def send_task_to_node(node, task):
    try:
        # Correct the URL to send tasks to the node
        task_url = node.replace('/api/metrics', '/api/tasks')
        response = requests.post(task_url, json=task)
        response.raise_for_status()
        logging.info(f"Task sent to {node} successfully")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send task to {node}: {e}")

def trigger_alerts(results):
    for node, alert in results:
        logging.warning(f"Alert triggered for {node}: {alert}")
        # Example alert triggering logic
        alert_message = {"alert": alert, "node": node}
        send_alert(node, alert_message)

def send_alert(node, alert_message):
    try:
        # Correct the URL to send alerts to the node
        alert_url = node.replace('/api/metrics', '/api/alerts')
        response = requests.post(alert_url, json=alert_message)
        response.raise_for_status()
        logging.info(f"Alert sent to {node} successfully")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send alert to {node}: {e}")

def display_results(results):
    for node, alert in results:
        logging.info(f"Node: {node}, Alert: {alert}")