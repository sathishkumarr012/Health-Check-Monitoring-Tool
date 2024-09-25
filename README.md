# HTTP Health Check Program

## Overview

This program monitors the health of a set of HTTP endpoints, checking their availability every 15 seconds and logging their availability percentage to the console. The endpoints and their request details are defined in a YAML configuration file. The program tests each endpoint's availability based on response codes and response times.

---

## Prerequisites

- **Python 3.x** (Make sure Python is installed)
- The following Python packages:
  - `requests`
  - `pyyaml`
  - `responses`

You can install these using `pip`.

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/sathishkumarr012/Health-Check-Monitoring-Tool.git
cd Health-Check-Monitoring-Tool
```

### 3. Create the `config.yaml` file

Create a `config.yaml` file with the following content:

```yaml
- headers:
    user-agent: fetch-synthetic-monitor
  method: GET
  name: fetch index page
  url: https://fetch.com/

- headers:
    user-agent: fetch-synthetic-monitor
  method: GET
  name: fetch careers page
  url: https://fetch.com/careers

- body: '{"foo":"bar"}'
  headers:
    content-type: application/json
    user-agent: fetch-synthetic-monitor
  method: POST
  name: fetch some fake post endpoint
  url: https://fetch.com/some/post/endpoint

- name: fetch rewards index page
  url: https://www.fetchrewards.com/
```

This file defines the endpoints that the program will check.

---

## Create a Virtual environment

### On macOS or Linux:

```bash
python3  -m venv venv
```

### On Windows:

```bash
python  -m venv venv
```

## Running the Program

You can run the program by passing the path to your `config.yaml` file as an argument. The program will run in an infinite loop until manually stopped.

### On macOS or Linux:

1. Activate your virtual environment (if you’re using one):

   ```bash
   source venv/bin/activate
   ```

### On Windows:

1. Activate your virtual environment (if you’re using one):

   ```bash
   .\venv\Scripts\activate
   ```

## Install The Required Python Packages
- Run the following Command to install the necessary packages:

```bash
pip install -r requirements.txt
```
If you don’t have a `requirements.txt`, create one with the following contents:

```text
requests
pyyaml
responses
```

## Run the script:

   ```bash
   python health_check.py config.yaml
   ```

Make sure to replace `config.yaml` with the full path to your YAML configuration file if it's located elsewhere.

---

## Program Output

The program will log the health check results every 15 seconds. Each cycle will print the status of the endpoints and the cumulative availability percentage of each domain.

Example output:

```
Starting test cycle #1...
Endpoint fetch.com index page has status: UP (Response code: 200, Response time: 0.1s)
Endpoint fetch.com careers page has status: DOWN (Response code: 200, Response time: 0.6s)
Endpoint fetch some fake post endpoint has status: DOWN (Response code: 500, Response time: 0.05s)
Endpoint fetch rewards index page has status: UP (Response code: 200, Response time: 0.1s)
fetch.com has 33% availability percentage
www.fetchrewards.com has 100% availability percentage
```

---

## Customization

To change the behavior of the program or to test different URLs and endpoints, modify the `config.yaml` file to match the structure of your desired endpoints.

---

## Stopping the Program

You can stop the program at any time by pressing `CTRL + C` in the terminal.

---

## Troubleshooting

### Common Errors:

1. **FileNotFoundError**:
   If you encounter a `FileNotFoundError`, ensure that the `config.yaml` file is in the correct directory or provide the full path to the file when running the script.

   Example:
   ```bash
   python health_check.py /full/path/to/config.yaml
   ```

2. **ModuleNotFoundError**:
   If you get a `ModuleNotFoundError` for `requests`, `pyyaml`, or `responses`, make sure to install the required packages:
   ```bash
   pip install requests pyyaml responses
   ```

---



