import schedule
import time
import subprocess
from ms_graph_grabber.data_grabber_flow import data_grabber_flow


# Schedule the script to be launched every day at a specific time (e.g., 8:00 AM)
schedule.every().day.at("19:05").do(data_grabber_flow)

# Message for the user
print("User's and device data will be updated at 19:05 Pacific Time")

while True:
    schedule.run_pending()
    time.sleep(1)
