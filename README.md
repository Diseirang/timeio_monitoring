# Install Library
  pip install pyTelegramBotAPI requests
# Create Python File In Your Prefer Directory
  exmaple.py
## Make the Python Script Executable

# Create a Systemd Service File
    sudo nano /etc/systemd/system/myscript.service

### Add some configure to your service file
    Ex : 
        Description=Run My Python Script
        After=network.target
        
        [Service]
        Type=simple
        ExecStart=/usr/bin/python3 /home/user/myscript.py
        Restart=always
        User=your-username
        WorkingDirectory=/home/user
        
        [Install]
        WantedBy=multi-user.target
