import json
from http.server import BaseHTTPRequestHandler, HTTPServer

class MockMetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/metrics':
            # metric yaha 
            metrics = {
                "metric1": 85,
                "metric2": 15
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(metrics).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/tasks':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            task = json.loads(post_data)
            print(f"Received task: {task}")
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "task received"}).encode('utf-8'))
        elif self.path == '/api/alerts':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            alert = json.loads(post_data)
            print(f"Received alert: {alert}")
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "alert received"}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=MockMetricsHandler, port=8001):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting mock worker node on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run(port=8001)