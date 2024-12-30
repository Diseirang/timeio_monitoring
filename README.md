# Install Library
  pip install pyTelegramBotAPI requests
# Create the Python Script
  e.g., /home/user/exmaple.py
# Make the Python Script Executable
  chmod +x /home/user/exmaple.py
# Write the Service File
  sudo nano /etc/systemd/system/exmaple.service
# Paste the following content into the service file:
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

# Reload Systemd and Enable the Service

  sudo systemctl daemon-reload
  sudo systemctl enable myscript.service
