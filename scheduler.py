import requests
import logging
from rules import RULES
import ctypes

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configuration of worker nodes
worker_nodes_api = ["http://localhost:8000/api/metrics", "http://localhost:8001/api/metrics",
                    "http://localhost:8002/api/metrics","http://localhost:8003/api/metrics"]

def collect_metrics():
    metrics = {}
    for node in worker_nodes_api:
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
        task = {"task": "tasklpuabcsfc", "node": node}
        send_task_to_node(node, task)

def send_task_to_node(node, task):
    try:
        task_url = node.replace('/api/metrics', '/api/tasks')
        response = requests.post(task_url, json=task)
        response.raise_for_status()
        logging.info(f"Task sent to {node} successfully")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send task to {node}: {e}")

def trigger_alerts(results):
    for node, alert in results:
        logging.warning(f"Alert triggered for {node}: {alert}")
        alert_message = {"alert": alert, "node": node}
        send_alert(node, alert_message)

def send_alert(node, alert_message):
    try:
        alert_url = node.replace('/api/metrics', '/api/alerts')
        response = requests.post(alert_url, json=alert_message)
        response.raise_for_status()
        logging.info(f"Alert sent to {node} successfully")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send alert to {node}: {e}")

def display_results(results):
    for node, alert in results:
        logging.info(f"Node: {node}, Alert: {alert}")

def allocate_memory(metrics):
    for node, node_metrics in metrics.items():
        memory_size = determine_memory_size(node_metrics)
        memory_location = allocate_memory_c(memory_size)
        logging.info(f"Allocated {memory_size} bytes at {memory_location} for {node}")

def determine_memory_size(metrics):
    # Example logic to determine memory size based on metrics
    return metrics.get("metric1", 0) * 1024  # Example: 1 KB per unit of metric1

def allocate_memory_c(size):
    # Call the C function to allocate memory
    lib = ctypes.CDLL('./memory_allocator.so')
    lib.allocate_memory.argtypes = [ctypes.c_size_t]
    lib.allocate_memory.restype = ctypes.c_void_p
    return lib.allocate_memory(size)