import logging
import schedule
import time
from api_data_grabber.data_grabber_flow import data_grabber_flow
from selector.сonfig import Config, get_config

# Define the time at which the script should be launched daily



def configure_logging():
    """
    Configures the logging settings for the script.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def schedule_data_grabbing(configuration:Config):
    """
    Schedules the data grabbing flow using the specified launch time.
    """
    # Schedule the script to be launched every day at a specific time
    schedule.every().day.at(configuration.connection_parameters['LAUNCH_TIME']).do(data_grabber_flow, configuration)


def main():
    """
    Main function that orchestrates the script's execution.
    """
    configure_logging()
    configuration = get_config()
    
    LAUNCH_TIME = configuration.connection_parameters['LAUNCH_TIME']
    try:
        schedule_data_grabbing(configuration=configuration)

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
