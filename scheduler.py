import schedule
import time
import subprocess


# Create a subprocess, which calls data grabber script
def launch_script():
    subprocess.call(['python', 'data_grabber_flow.py'])

# Schedule the script to be launched every day at a specific time (e.g., 8:00 AM)
schedule.every().day.at("21:05").do(launch_script)

# Message for the user
print("User's and device data will be updated at 21:05 Pacific Time")

while True:
    schedule.run_pending()
    time.sleep(1)