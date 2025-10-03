# Testing by mengheak

import os
import requests
from datetime import date, datetime, timedelta
import configparser

# Load configuration
config = configparser.ConfigParser()
config.read("configss.properties")

BOT_TOKEN = config["DEFAULT"]["BOT_TOKEN"]
CHAT_ID = config["DEFAULT"]["CHAT_ID"]

# Parse host details from the configuration
HOSTS = {key: value for key, value in config["HOSTS"].items() if key.lower() not in ["bot_token", "chat_id"]}
PC_IP = list(HOSTS.values())
HOST_NAMES = list(HOSTS.keys())

# State tracking
last_status = {ip: None for ip in PC_IP}
last_seen = {ip: datetime.now() for ip in PC_IP}

# Quiet hours (adjust as needed)
QUIET_HOURS_START = 23  # 11 PM
QUIET_HOURS_END = 6  # 6 AM

def is_quiet_hours():
    """Checks if the current time is within quiet hours."""
    current_hour = datetime.now().hour
    return QUIET_HOURS_START <= current_hour or current_hour < QUIET_HOURS_END

def send_telegram_notification(message):
    """Sends a notification to Telegram, unless it's quiet hours."""
    if is_quiet_hours():
        print(f"Quiet hours active. Notification suppressed: {message}")
        return

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

        DEVICE_LOCATION = get_device_info(ip).upper()
        CURRENT_DATE = date.today().strftime('%B %d, %Y')
        CURRENT_TIME = datetime.now().strftime('%H:%M:%S %p')

        if online_status:
            if last_status[ip] != True:
                MESSAGE = (
                    f"🚨TimeIO Notification Alert🚨\n\n"
                    f"Location: {DEVICE_LOCATION}\n"
                    f"IP: {ip}\n"
                    f"Date: {CURRENT_DATE}\n"
                    f"Time: {CURRENT_TIME}"
                )
                send_telegram_notification(f"{MESSAGE}\nStatus: UP! 📶✅\n")
                last_status[ip] = True

            # update last seen if online
            last_seen[ip] = datetime.now()

        else:  # device offline
            elapsed_time = datetime.now() - last_seen[ip]
            if elapsed_time > timedelta(minutes=1) and last_status[ip] != False:
                MESSAGE = (
                    f"🚨TimeIO Notification Alert🚨\n\n"
                    f"Location: {DEVICE_LOCATION}\n"
                    f"IP: {ip}\n"
                    f"Date: {CURRENT_DATE}\n"
                    f"Time: {CURRENT_TIME}"
                )
                send_telegram_notification(f"{MESSAGE}\nStatus: DOWN! ❌❌\n")
                last_status[ip] = False
