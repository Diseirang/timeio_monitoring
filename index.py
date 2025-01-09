import os
import requests
from datetime import date , datetime
import time


# Configuration
PC_IP = ["10.16.181.137", "10.16.179.132", "10.21.2.58"]  # Replace with your PC's IPs or hostnames
MACHINE_NAME = ["Villa4 TimeIO","Villa4 TimeIO","Diseirang"]
LOCATIONS = ["Villa4 Academic Office","Villa4 Lobby","Diseirang"]

BOT_TOKEN = "7810489769:AAH_SQqIj8meDEpaDqO_x0bQChTcON1YfPA"
CHAT_ID = "-1002402001672"
# CHECK_INTERVAL = 60  # Check every 1 minutes

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

# State tracking
last_status = {ip: None for ip in PC_IP}  # Track the status of each IP
timeout_counter = {ip: 0 for ip in PC_IP}  # Track the number of consecutive timeouts for each IP

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
    # INDEX_OF_PCIP = PC_IP.index(ip)
    if ip == PC_IP[0] :
        DEVICE_NAME = MACHINE_NAME[0]
        LOCATION= LOCATIONS[0]
            
    elif ip == PC_IP[1] :
        DEVICE_NAME = MACHINE_NAME[1]
        LOCATION= LOCATIONS[1]
    
    elif ip == PC_IP[2] :
        DEVICE_NAME = MACHINE_NAME[2]
        LOCATION= LOCATIONS[2]
        
    return DEVICE_NAME,LOCATION

while True:
    for ip in PC_IP:
        online_status = is_device_online(ip)
                
        DEVICE_NAME, LOCATION = check_device_name(PC_IP, MACHINE_NAME, LOCATIONS, ip) 

        CURRENT_DATE =  date.today().strftime('%B %d, %Y')
        CURRENT_TIME =  datetime.now().strftime('%H:%M:%S %p')

        if online_status:
            # Reset the timeout counter if the device is online
            if timeout_counter[ip] > 0:
                timeout_counter[ip] = 0
            
            print(timeout_counter[ip])

            if online_status != last_status[ip]:  # Send notification only if status changes
                MESSAGE = f"🚨TimeIO Notification Alert🚨\n\nDevice name: {DEVICE_NAME}\nLocation: {LOCATION}\nDate: {CURRENT_DATE}\nTime: {CURRENT_TIME}"
                send_telegram_notification(f"{MESSAGE}\nStatus: UP! 📶✅\n")
                last_status[ip] = online_status        
        else:
            # Increment the timeout counter for offline devices
            timeout_counter[ip] += 1
            print(timeout_counter[ip])
            if timeout_counter[ip] == 5:  # Send notification only after 5 consecutive timeouts
                MESSAGE = f"🚨TimeIO Notification Alert🚨\n\nDevice name: {DEVICE_NAME}\nLocation: {LOCATION}\nDate: {CURRENT_DATE}\nTime: {CURRENT_TIME}"
                send_telegram_notification(f"{MESSAGE}\nStatus: DOWN! ❌❌\n")
                last_status[ip] = online_status

    # time.sleep(CHECK_INTERVAL)  # Wait before the next check

# if __name__  == "__main__":
#     while True:
#         main()