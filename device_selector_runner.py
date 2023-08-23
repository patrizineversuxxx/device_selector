import logging
from selector.main import device_selector_flow

def main():
    try:
        device_selector_flow()
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    main()