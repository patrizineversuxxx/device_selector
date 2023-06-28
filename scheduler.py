import schedule
import time
import subprocess

def launch_script():
    # Replace 'script_to_launch.py' with the name of the Python script you want to launch
    subprocess.call(['python', 'data_grabber_flow.py'])

# Schedule the script to be launched every day at a specific time (e.g., 8:00 AM)
schedule.every().day.at("21:05").do(launch_script)
#schedule.every().hour.at("03:25").do(launch_script())

while True:
    schedule.run_pending()
    time.sleep(1)