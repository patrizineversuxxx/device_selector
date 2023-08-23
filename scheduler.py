import logging
import schedule
import time
from ms_graph_grabber.data_grabber_flow import data_grabber_flow

# Define the time at which the script should be launched daily
LAUNCH_TIME = "19:05"


def configure_logging():
    """
    Configures the logging settings for the script.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def schedule_data_grabbing():
    """
    Schedules the data grabbing flow using the specified launch time.
    """
    # Schedule the script to be launched every day at a specific time
    schedule.every().day.at(LAUNCH_TIME).do(data_grabber_flow)


def main():
    """
    Main function that orchestrates the script's execution.
    """
    configure_logging()

    try:
        schedule_data_grabbing()

        # Message for the user
        logging.info(
            f"User's and device data will be updated at {LAUNCH_TIME} Pacific Time")

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
