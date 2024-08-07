import json
import yaml
import datetime
from jinja2 import Template

DATA_FILE = "data.json"
INCIDENT_FILE = "incident.yaml"
STATUS_PAGE = "index.html"
TEMPLATE_FILE = "template.html"

# Ensure data.json exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as file:
        json.dump([], file)

# Ensure incident.yaml exists
if not os.path.exists(INCIDENT_FILE):
    with open(INCIDENT_FILE, "w") as file:
        yaml.dump({"incidents": []}, file)

def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data

def load_incidents():
    try:
        with open(INCIDENT_FILE, "r") as file:
            incidents = yaml.safe_load(file)
    except FileNotFoundError:
        incidents = {"incidents": []}
    
    # Ensure incidents is a dictionary and has the key "incidents"
    if not isinstance(incidents, dict) or "incidents" not in incidents:
        return []
    
    return incidents["incidents"]

def calculate_uptime(data):
    total_checks = len(data)
    up_checks = sum(1 for record in data if record["status"])
    uptime_percentage = round((up_checks / total_checks) * 100) if total_checks else 0
    return uptime_percentage

def filter_response_time(data):
    # Filter out records with null response time
    data = [record for record in data if record["response_time"] is not None]
    # Sort by timestamp
    data.sort(key=lambda x: x["timestamp"])
    # Get the latest 30 values
    return data[-30:]

def prepare_uptime_data(data):
    daily_status = {}
    for record in data:
        date = record["timestamp"].split("T")[0]
        if date not in daily_status:
            daily_status[date] = {"up": 0, "down": 0}
        if record["status"]:
            daily_status[date]["up"] += 1
        else:
            daily_status[date]["down"] += 1
    
    uptime_data = []
    for date, status in sorted(daily_status.items()):
        if status["down"] == 0:
            uptime_data.append({"date": date, "color": "green"})
        elif status["up"] == 0:
            uptime_data.append({"date": date, "color": "red"})
        else:
            uptime_data.append({"date": date, "color": "yellow"})
    
    return uptime_data

def generate_graph_data(data):
    response_data = filter_response_time(data)
    timestamps = [record["timestamp"] for record in response_data]
    response_times = [record["response_time"] * 1000 for record in response_data]  # Convert to ms

    return {
        "timestamps": timestamps,
        "response_times": response_times
    }

def generate_page(data, incidents):
    uptime_percentage = calculate_uptime(data)
    graph_data = generate_graph_data(data)
    uptime_data = prepare_uptime_data(data)

    with open(TEMPLATE_FILE, "r") as file:
        template_content = file.read()
        
    template = Template(template_content)

    html_content = template.render(
        uptime_percentage=uptime_percentage,
        incidents=incidents,
        graph_data=graph_data,
        uptime_data=uptime_data
    )

    with open(STATUS_PAGE, "w") as file:
        file.write(html_content)

def main():
    data = load_data()
    incidents = load_incidents()
    generate_page(data, incidents)

if __name__ == "__main__":
    main()
