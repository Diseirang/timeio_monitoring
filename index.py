import os
import requests
from datetime import date , datetime
import configparser
import logging

# Configure logging
logging.basicConfig(
    filename='index.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load configuration
config = configparser.ConfigParser()
config.read("configure.properties")

BOT_TOKEN = config["DEFAULT"]["BOT_TOKEN"]
CHAT_ID = config["DEFAULT"]["CHAT_ID"]

# Parse host details from the configuration
HOSTS = {
    key: value for key, 
    value in config["HOSTS"].items() 
    if key.lower() not in ["bot_token", "chat_id"]
    }

PC_IP = list(HOSTS.values())
HOST_NAMES = list(HOSTS.keys())

# State tracking
last_status = {ip: None for ip in PC_IP}
timeout_counter = {ip: 0 for ip in PC_IP}

def send_telegram_notification(message):
    """Sends a notification to Telegram."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            logging.info(f"Notification sent: {message}")
        else:
            logging.warning(f"Failed to send notification: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending notification: {e}")

def is_device_online(ip):
    """Checks if a device is online."""
    try:
        response = os.system(f"ping -c 1 {ip} > /dev/null 2>&1" if os.name != "nt" else f"ping -n 1 {ip} > nul")
        return response == 0
    except Exception as e:
        logging.error(f"Error pinging {ip}: {e}")
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
            if timeout_counter[ip] > 0:
                timeout_counter[ip] = 0

            if online_status != last_status[ip]:
                logging.debug(f"{timeout_counter[ip]} : {ip}")
                MESSAGE = f"🚨TimeIO Notification Alert🚨\n\nDevice Name: {DEVICE_NAME}\nIP: {ip}\nDate: {CURRENT_DATE}\nTime: {CURRENT_TIME}"
                send_telegram_notification(f"{MESSAGE}\nStatus: UP! 📶✅\n")
                last_status[ip] = online_status        
        else:
            timeout_counter[ip] += 1
            logging.debug(f"{timeout_counter[ip]} : {ip}")

            if timeout_counter[ip] == 5:
                logging.debug(f"{timeout_counter[ip]} : {ip}")
                MESSAGE = f"🚨TimeIO Notification Alert🚨\n\nHost Name: {DEVICE_NAME}\nIP: {ip}\nDate: {CURRENT_DATE}\nTime: {CURRENT_TIME}"
                send_telegram_notification(f"{MESSAGE}\nStatus: DOWN! ❌❌\n")
                last_status[ip] = online_status