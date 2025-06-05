from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import requests
from datetime import date, datetime, time
import configparser
import logging
import subprocess

config = configparser.ConfigParser()
config.read("config_tak_ais.properties")

BOT_TOKEN = config["DEFAULT"]["BOT_TOKEN"]
CHAT_ID = config["DEFAULT"]["CHAT_ID"]

HOSTS = {key: value for key, value in config["HOSTS"].items() if key.lower() not in ["bot_token", "chat_id"]}
PC_IP = list(HOSTS.values())
HOST_NAMES = list(HOSTS.keys())

# State tracking
last_status = {ip: None for ip in PC_IP}
timeout_counter = {ip: 0 for ip in PC_IP}

os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename="logs/tak_ais_monitoring.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
    
def monitor_hosts():
    with ThreadPoolExecutor(max_workers=len(PC_IP)) as executor:
        future_to_ip = {executor.submit(is_device_online, ip): ip for ip in PC_IP}
        for future in as_completed(future_to_ip):
            ip, online_status = future.result()
            device_location = get_device_info(ip).upper()
            current_date = date.today().strftime('%B %d, %Y')
            current_time = datetime.now().strftime('%H:%M:%S %p')

            message = (
                f"🚨AIS_TAK Notification Alert🚨\n\n"
                f"Location: {device_location}\n"
                f"IP: {ip}\n"
                f"Date: {current_date}\n"
                f"Time: {current_time}"
            )

            if online_status:
                if timeout_counter[ip] > 0:
                    timeout_counter[ip] = 0

                if last_status[ip] != online_status:
                    send_telegram_notification(f"{message}\nStatus: UP! 📶✅\n")
                    last_status[ip] = online_status
            else:
                timeout_counter[ip] += 1
                if timeout_counter[ip] == 10:
                    send_telegram_notification(f"{message}\nStatus: DOWN! ❌❌\n")
                    last_status[ip] = online_status

if __name__ == "__main__":
    while True:
        monitor_hosts()
        time.sleep(5)  # Adjust the interval as needed