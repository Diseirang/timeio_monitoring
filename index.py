import os
import requests
from datetime import date , datetime
import configparser

# Load configuration
config = configparser.ConfigParser()
config.read("configure.properties")
BOT_TOKEN = config["DEFAULT"]["BOT_TOKEN"]
CHAT_ID = config["DEFAULT"]["CHAT_ID"]

# Parse host details from the configuration
hosts = dict(config["HOSTS"])  # Converts [HOSTS] section into a dictionary
PC_IP = list(hosts.values())
HOST_NAMES = list(hosts.keys())

# State tracking
last_status = {ip: None for ip in PC_IP}  # Track the status of each IP
timeout_counter = {ip: 0 for ip in PC_IP}  # Track the number of consecutive timeouts for each IP


def send_telegram_notification(message):
    """Sends a notification to Telegram."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print(f"Notification sent: {message}")
        else:
            print(f"Failed to send notification: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending notification: {e}")

def is_device_online(ip):
    """Checks if a device is online."""
    try:
        # Ping the device
        response = os.system(f"ping -c 1 {ip} > /dev/null 2>&1" if os.name != "nt" else f"ping -n 1 {ip} > nul")
        return response == 0
    except Exception as e:
        print(f"Error pinging {ip}: {e}")
        return False
    
def get_device_info(ip):
    """Returns the host name for the given IP."""
    try:
        index = PC_IP.index(ip)
        return HOST_NAMES[index]
    except ValueError:
        return "Unknown Host"

while True:
    for ip in PC_IP:
        online_status = is_device_online(ip)
                
        DEVICE_NAME = get_device_info(ip) 

        CURRENT_DATE =  date.today().strftime('%B %d, %Y')
        CURRENT_TIME =  datetime.now().strftime('%H:%M:%S %p')

        if online_status:
            # Reset the timeout counter if the device is online
            if timeout_counter[ip] > 0:
                timeout_counter[ip] = 0
            
            print(timeout_counter[ip])

            if online_status != last_status[ip]:  # Send notification only if status changes
                MESSAGE = f"🚨TimeIO Notification Alert🚨\n\nDevice name: {DEVICE_NAME} : {ip}\nDate: {CURRENT_DATE}\nTime: {CURRENT_TIME}"
                send_telegram_notification(f"{MESSAGE}\nStatus: UP! 📶✅\n")
                last_status[ip] = online_status        
        else:
            # Increment the timeout counter for offline devices
            timeout_counter[ip] += 1
            print(timeout_counter[ip])
            if timeout_counter[ip] == 5:  # Send notification only after 5 consecutive timeouts
                MESSAGE = f"🚨TimeIO Notification Alert🚨\n\nDevice name: {DEVICE_NAME} : {ip}\nDate: {CURRENT_DATE}\nTime: {CURRENT_TIME}"
                send_telegram_notification(f"{MESSAGE}\nStatus: DOWN! ❌❌\n")
                last_status[ip] = online_status