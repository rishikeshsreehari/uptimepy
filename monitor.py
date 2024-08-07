import requests
import json
import datetime
import smtplib
from email.mime.text import MIMEText
import yaml
import os

URL = "http://rishikeshs.com"
DATA_FILE = "data.json"
INCIDENT_FILE = "incident.yaml"
EMAIL = "your-email@gmail.com"
EMAIL_PASSWORD = "your-email-password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
CHECK_INTERVAL = 15  # in minutes

def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, EMAIL_PASSWORD)
            server.sendmail(EMAIL, [EMAIL], msg.as_string())
        print("Downtime email sent successfully")
    except Exception as e:
        print(f"Website down, but unable to send email: {e}")

def check_website():
    try:
        response = requests.get(URL, timeout=10)
        status = response.status_code == 200
        response_time = response.elapsed.total_seconds()
    except requests.RequestException:
        status = False
        response_time = None

    return status, response_time

def update_data(status, response_time):
    now = datetime.datetime.now().isoformat()
    data = {"timestamp": now, "status": status, "response_time": response_time}

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            records = json.load(file)
    else:
        records = []

    records.append(data)

    # Keep records for the last 12 months
    cutoff = datetime.datetime.now() - datetime.timedelta(days=365)
    records = [record for record in records if datetime.datetime.fromisoformat(record["timestamp"]) > cutoff]

    with open(DATA_FILE, "w") as file:
        json.dump(records, file, indent=4)

    if not status:
        record_incident(now)

def record_incident(timestamp):
    incident = {"timestamp": timestamp, "reason": "Unknown", "status": "down"}
    
    if os.path.exists(INCIDENT_FILE):
        with open(INCIDENT_FILE, "r") as file:
            incidents = yaml.safe_load(file)
    else:
        incidents = {"incidents": []}

    incidents["incidents"].append(incident)
    
    with open(INCIDENT_FILE, "w") as file:
        yaml.safe_dump(incidents, file)

def main():
    status, response_time = check_website()
    if status:
        print(f"Website is up with a response time of {response_time:.2f} seconds.")
    else:
        print(f"Website is down as of {datetime.datetime.now().isoformat()}")

    update_data(status, response_time)

    if not status:
        send_email("Website Down", f"The website {URL} is down as of {datetime.datetime.now().isoformat()}.")

if __name__ == "__main__":
    main()
