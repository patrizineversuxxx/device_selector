import logging
from selector.main import device_selector_flow

def main():
    """
    Entry point of the script. Executes the device_selector_flow function and handles exceptions.

    This function sets up logging, calls the device_selector_flow function, and catches any exceptions that occur.
    If an exception is caught, it logs an error message.

    Args:
        None

    Returns:
        None
    """
    try:
        device_selector_flow()
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    # Configure logging to display information with the desired format
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Call the main function to start the script
    main()
