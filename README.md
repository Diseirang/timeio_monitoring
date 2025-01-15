# 1. Install Library
  ```
  pip install pyTelegramBotAPI requests
  ```
# 2. Create the Python Script
  e.g., /home/user/exmaple.py
# 3. Make the Python Script Executable
  ```
  chmod +x /home/user/exmaple.py
  ```
# 4. Write the Service File
  ```
  sudo nano /etc/systemd/system/exmaple.service
  ```
# 5. Paste the following content into the service file:
  ```
  [Unit]
  Description=Run My Python Script
  After=network.target
  
  [Service]
  Type=simple
  ExecStart=/usr/bin/python3 /home/user/exmaple.py
  Restart=always
  User=your-username
  WorkingDirectory=/home/user
  
  [Install]
  WantedBy=multi-user.target
  ```
# 6. Reload Systemd and Enable the Service

  ```
  sudo systemctl daemon-reload
  sudo systemctl enable myscript.service
  ```
# 7. Start and Test the Service
  ## Start the service with:
  ```
  sudo systemctl start myscript.service
  ```
  ## Check the status to ensure it's running:
  ```
  sudo systemctl status myscript.service
  ```


# Required Python 3.12 up to run this project properly
