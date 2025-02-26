import os
import requests
from datetime import date, datetime, timedelta
import configparser
import logging
import subprocess

# Load configuration
config = configparser.ConfigParser()
# config.read("config_tsk.properties")
config.read("config_ccv_aii.properties")

BOT_TOKEN = config["DEFAULT"]["BOT_TOKEN"]
CHAT_ID = config["DEFAULT"]["CHAT_ID"]

# print(CHAT_ID)

# Parse host details from the configuration
HOSTS = {key: value for key, value in config["HOSTS"].items() if key.lower() not in ["bot_token", "chat_id"]}
PC_IP = list(HOSTS.values())
HOST_NAMES = list(HOSTS.keys())

# State tracking
last_status = {ip: None for ip in PC_IP}
last_seen = {ip: datetime.now() for ip in PC_IP}

os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename="logs/monitor_ccv_ais.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def send_telegram_notification(message):
    """Sends a notification to Telegram."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            logging.info(f"Notification sent: {message}")
        else:
            logging.error(f"Failed to send notification: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        logging.critical(f"Error sending notification: {e}")

def is_device_online(ip):
    """Checks if a device is online using a ping command (Linux/macOS only)."""
    try:
        # Run the ping command with -c 1 (Linux/macOS)
        command = ["ping", "-c", "1", ip]
        result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0
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
                
        DEVICE_LOCATION = get_device_info(ip).upper()
        CURRENT_DATE = date.today().strftime('%B %d, %Y')
        CURRENT_TIME = datetime.now().strftime('%H:%M:%S %p')
        
        MESSAGE = f"🚨Aii-CCV Notification Alert🚨\n\nLocation: {DEVICE_LOCATION}\nIP: {ip}\nDate: {CURRENT_DATE}\nTime: {CURRENT_TIME}"

        if online_status:
            # Device is online
            if last_status[ip] != True:
                send_telegram_notification(f"{MESSAGE}\nStatus: UP! 📶✅\n")
                last_status[ip] = True
            # Update last seen timestamp
            last_seen[ip] = datetime.now()
        else:
            # Device is offline
            elapsed_time = datetime.now() - last_seen[ip]
            if elapsed_time > timedelta(minutes=1) and last_status[ip] != False:
                send_telegram_notification(f"{MESSAGE}\nStatus: DOWN! ❌❌\n")
                last_status[ip] = False
