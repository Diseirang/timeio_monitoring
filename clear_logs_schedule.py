#!/usr/bin/env python3

import os
import shutil
from datetime import datetime
import logging

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename="logs/clear_logs.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def clear_logs_once_a_month(log_dir="logs"):
    """Clears all files in the logs folder on the first day of each month."""
    today = datetime.today()
    if today.day == 1:
        logging.info("First day of the month - clearing logs.")
        for filename in os.listdir(log_dir):
            file_path = os.path.join(log_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    logging.info(f"Deleted log file: {file_path}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    logging.info(f"Deleted log directory: {file_path}")
            except Exception as e:
                logging.error(f"Error deleting {file_path}: {e}")
    else:
        logging.info("Not the first day of the month. Skipping cleanup.")

if __name__ == "__main__":
    clear_logs_once_a_month()
