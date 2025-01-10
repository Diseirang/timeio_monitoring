import os
import requests
from datetime import date , datetime
import time

# Configuration
PC_IP = ["10.23.46.27", "10.23.46.26", "10.23.46.37","10.23.46.29"]  # Replace with your PC's IPs or hostnames
MACHINE_NAME = ["Student Card 1","Student Card 2","Staff TimeIO"]
LOCATIONS = ["Lobby","3rd Floor"]
BUILDING = "Admin Building SenSok"

BOT_TOKEN = "7820861130:AAEkXmZlNsJrHxDrBWakH-XzeC893mYwHNQ"
CHAT_ID = "-1002428026884"
CHECK_INTERVAL = 60  # Check every 2 minutes

DEVICE_NAME = None
LOCATION = None
MESSAGE = None

# State tracking
last_status = {ip: None for ip in PC_IP}  # Track the status of each IP

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
    
def check_device_name(PC_IP, MACHINE_NAME, LOCATIONS, ip):
    if ip == PC_IP[0] :
        DEVICE_NAME = MACHINE_NAME[0]
        LOCATION= LOCATIONS[0]
            
    elif ip == PC_IP[1] :
        DEVICE_NAME = MACHINE_NAME[1]
        LOCATION= LOCATIONS[0]
            
    elif ip == PC_IP[2] :
        DEVICE_NAME = MACHINE_NAME[2]
        LOCATION= LOCATIONS[0]
            
    elif ip == PC_IP[3] :
        DEVICE_NAME = MACHINE_NAME[2]
        LOCATION= LOCATIONS[1]
        
    return DEVICE_NAME,LOCATION

while True:
    for ip in PC_IP:
        online_status = is_device_online(ip)
                
        DEVICE_NAME, LOCATION = check_device_name(PC_IP, MACHINE_NAME, LOCATIONS, ip) 

        CURRENT_DATE =  date.today()
        CURRENT_TIME =  datetime.now()

        if online_status != last_status[ip]:  # Send notification only if status changes
            MESSAGE = f"🚨Staff&Student TimeIO Alert🚨\n\nDevice name: {DEVICE_NAME}\nLocation: {LOCATION}\nBuilding: {BUILDING}\nDate: {CURRENT_DATE.strftime('%B %d, %Y') }\nTime: { CURRENT_TIME.strftime('%H:%M:%S %p')}"
            if online_status:
                send_telegram_notification(f"{MESSAGE}\nStatus: UP! 📶✅\n")
            else:
                send_telegram_notification(f"{MESSAGE}\nStatus: DOWN! ❌❌\n")
            last_status[ip] = online_status  # Update the last known status for this IP

    time.sleep(CHECK_INTERVAL)  # Wait before the next check
