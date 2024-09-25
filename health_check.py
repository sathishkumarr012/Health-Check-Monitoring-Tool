import requests
import yaml
import time
import sys
import responses

# Global variable to track the number of cycles
cycle_count = 0

# Function to parse the YAML configuration file
def parse_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Mock responses to simulate different behavior for different test cycles
def register_responses():
    global cycle_count

    # Registering responses for each cycle without clearing previous mocks
    if cycle_count == 0:
        # Test cycle #1
        responses.add(responses.GET, "https://fetch.com/", json={}, status=200, adding_headers={'elapsed-time': '0.1'})  # Latency 100ms
        responses.add(responses.GET, "https://fetch.com/careers", json={}, status=200, adding_headers={'elapsed-time': '0.6'})  # Latency 600ms
        responses.add(responses.POST, "https://fetch.com/some/post/endpoint", json={}, status=500, adding_headers={'elapsed-time': '0.05'})  # Latency 50ms
        responses.add(responses.GET, "https://www.fetchrewards.com/", json={}, status=200, adding_headers={'elapsed-time': '0.1'})  # Latency 100ms

    elif cycle_count == 1:
        # Test cycle #2
        responses.add(responses.GET, "https://fetch.com/", json={}, status=200, adding_headers={'elapsed-time': '0.1'})  # Latency 100ms
        responses.add(responses.GET, "https://fetch.com/careers", json={}, status=200, adding_headers={'elapsed-time': '0.3'})  # Latency 300ms
        responses.add(responses.POST, "https://fetch.com/some/post/endpoint", json={}, status=201, adding_headers={'elapsed-time': '0.05'})  # Latency 50ms
        responses.add(responses.GET, "https://www.fetchrewards.com/", json={}, status=200, adding_headers={'elapsed-time': '0.9'})  # Latency 900ms

    else:
        # Test cycle #3 and beyond
        responses.add(responses.GET, "https://fetch.com/", json={}, status=200, adding_headers={'elapsed-time': '0.1'})  # Latency 100ms
        responses.add(responses.GET, "https://fetch.com/careers", json={}, status=200, adding_headers={'elapsed-time': '0.3'})  # Latency 300ms
        responses.add(responses.POST, "https://fetch.com/some/post/endpoint", json={}, status=201, adding_headers={'elapsed-time': '0.05'})  # Latency 50ms
        responses.add(responses.GET, "https://www.fetchrewards.com/", json={}, status=200, adding_headers={'elapsed-time': '0.9'})  # Latency 900ms

# Function to send HTTP requests and mock responses
@responses.activate
def send_request(endpoint):
    register_responses()
    method = endpoint.get('method', 'GET')
    url = endpoint['url']

    try:
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error making request to {url}: {e}")
        return None

# Function to check if the response is UP or DOWN
def check_health(response):
    if response is None:
        return 'DOWN'
    
    elapsed_time = float(response.headers.get('elapsed-time', '0.0'))
    if 200 <= response.status_code < 300 and elapsed_time < 0.5:
        return 'UP'
    else:
        return 'DOWN'

# Function to update availability statistics
availability = {}
def update_availability(domain, status):
    if domain not in availability:
        availability[domain] = {'up': 0, 'total': 0}
    availability[domain]['total'] += 1
    if status == 'UP':
        availability[domain]['up'] += 1

# Function to log the availability percentages
def log_availability():
    for domain, stats in availability.items():
        percentage = 100 * (stats['up'] / stats['total'])
        print(f"{domain} has {round(percentage)}% availability percentage")

# Main function to run health checks
def run_health_checks(endpoints):    
    global cycle_count
    while True:
        print(f"Starting test cycle #{cycle_count + 1}...")
        for endpoint in endpoints:
            response = send_request(endpoint)
            status = check_health(response)
            domain = endpoint['url'].split('/')[2]  # Extract the domain from the URL
            
            if response is None:
                print(f"Failed to get a response from {endpoint['url']}. Marking as DOWN.")
                status = 'DOWN'
            else:
                print(f"Endpoint {endpoint['name']} has status: {status} (Response code: {response.status_code}, Response time: {response.headers['elapsed-time']}s)")

            update_availability(domain, status)

        log_availability()
        cycle_count += 1
        time.sleep(15)  # Wait for 15 seconds before the next check cycle

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python health_check.py <config_file.yaml>")
        sys.exit(1)

    config_file = sys.argv[1]
    endpoints = parse_yaml(config_file)
    run_health_checks(endpoints)