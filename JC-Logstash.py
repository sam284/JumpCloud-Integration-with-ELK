import socket
import datetime
import json
import requests
import time


# Define the Logstash server's host and port
logstash_host = "localhost"
logstash_port = 65040  # Change to your desired port

jcapikey = "" #Add your Jumpcloud API Key Here
incrementAmount = 60
service = ["directory", "sso", "systems", "software", "radius"]
now = datetime.datetime.utcnow()
start_dt = now - datetime.timedelta(minutes=incrementAmount)
start_date = start_dt.isoformat("T") + "Z"
end_date = now.isoformat("T") + "Z"

# Initialize an empty list to store logs
logs = []

for service in service:
    url = "https://api.jumpcloud.com/insights/directory/v1/events"

    payload = {
        "end_time": end_date,
        "service": [f"{service}"],
        "start_time": start_date
    }
    headers = {
        "accept": "application/json",
        "x-api-key": jcapikey,
        "content-type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    #print (response.text)
    if response.status_code == 200:
        # Parse the JSON response content
        response_json = response.json()
        #print (response_json)
        if isinstance(response_json, list):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((logstash_host, logstash_port))
                    for obj in response_json:
                        log_data = json.dumps(obj)
                        log_data_bytes = log_data.encode()
                        log_data_bytes += b"\n"
                        s.sendall(log_data_bytes)
                        time.sleep(1)
                        #print (log_data_bytes)
                        print(f"Object sent:\n {log_data_bytes}")
            except Exception as e:
                print(f"Error sending object to Logstash: {str(e)}")
