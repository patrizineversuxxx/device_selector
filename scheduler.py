import logging
import schedule
import time
from ms_graph_grabber.data_grabber_flow import data_grabber_flow

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def schedule_data_grabbing():
    # Schedule the script to be launched every day at a specific time (e.g., 19:05)
    schedule.every().day.at("19:05").do(data_grabber_flow)

def main():
    configure_logging()

    try:
        schedule_data_grabbing()

        # Message for the user
        print("User's and device data will be updated at 19:05 Pacific Time")

        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Script stopped by user.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Entry point of the script
if __name__ == "__main__":
    main()
