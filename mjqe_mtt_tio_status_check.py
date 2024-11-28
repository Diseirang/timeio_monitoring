import os
import requests
from datetime import date , datetime
import time


# Configuration
PC_IP = ["10.16.181.137", "10.16.179.132 ", "10.16.181.136","10.16.179.203","10.15.53.13","10.15.54.72","10.15.51.10","10.15.54.253","10.15.51.28","10.16.190.157"]  # Replace with your PC's IPs or hostnames
MACHINE_NAME = ["Villa4 TimeIO","Villa4 TimeIO","MJQE TimeIO","NH TimeIO","QLH TimeIO","LKN TimeIO","MJQR TimeIO"]
LOCATIONS = ["Villa4 Academic Office","Villa4 Lobby","MJQE 6th floor","MJQE Lobby","NH Academic Office","QLH 12th Floor","QLH Lobby","LKN 12th Floor","LKN Lobby","Mezzanine Floor"]

BOT_TOKEN = "7232990613:AAEka4GKSoFCgTzqcNYyygSZRoqcswmwUOU"
CHAT_ID = "-1002267980034"
CHECK_INTERVAL = 60  # Check every 1 minutes

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
        LOCATION= LOCATIONS[1]
            
    elif ip == PC_IP[2] :
        DEVICE_NAME = MACHINE_NAME[2]
        LOCATION= LOCATIONS[2]
            
    elif ip == PC_IP[3] :
        DEVICE_NAME = MACHINE_NAME[2]
        LOCATION= LOCATIONS[3]
            
    elif ip == PC_IP[4] :
        DEVICE_NAME = MACHINE_NAME[3]
        LOCATION= LOCATIONS[4]
    
    elif ip == PC_IP[5] :
        DEVICE_NAME = MACHINE_NAME[4]
        LOCATION= LOCATIONS[5]
            
    elif ip == PC_IP[6] :
        DEVICE_NAME = MACHINE_NAME[4]
        LOCATION= LOCATIONS[6]
            
    elif ip == PC_IP[7] :
        DEVICE_NAME = MACHINE_NAME[5]
        LOCATION= LOCATIONS[7]
            
    elif ip == PC_IP[8] :
        DEVICE_NAME = MACHINE_NAME[5]
        LOCATION= LOCATIONS[8]
	elif ip == PC_IP[9] :
		DEVICE_NAME = MACHINE_NAME[6]
		LOCATION = LOCATIONS[9]
        
    return DEVICE_NAME,LOCATION

while True:
    for ip in PC_IP:
        online_status = is_device_online(ip)
                
        DEVICE_NAME, LOCATION = check_device_name(PC_IP, MACHINE_NAME, LOCATIONS, ip) 

        CURRENT_DATE =  date.today()
        CURRENT_TIME =  datetime.now()

        if online_status != last_status[ip]:  # Send notification only if status changes
            MESSAGE = f"🚨TimeIO Notification Alert🚨\n\nDevice name: {DEVICE_NAME}\nLocation: {LOCATION}\nDate: {CURRENT_DATE.strftime('%B %d, %Y') }\nTime: { CURRENT_TIME.strftime('%H:%M:%S %p')}"
            if online_status:
                print(f"{MESSAGE}\nStatus: UP! 📶✅\n")
            else:
                print(f"{MESSAGE}\nStatus: DOWN! ❌❌\n")
            last_status[ip] = online_status  # Update the last known status for this IP

    time.sleep(CHECK_INTERVAL)  # Wait before the next check
