import time
import requests
import concurrent.futures
import typing
import logging

# Tuple of naming tags, used for identifying Pilot Groups
PILOT_GROUPS_NAMING_TAGS = ("POC", "UAT", "_test_vneskorodov", "pilot")
# Constant for storing API Base URL (Microsoft Graph API base)
API_BASE_URL = "https://graph.microsoft.com/beta"

# Configure logging service
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function for formatting elapsed time from seconds to minutes and seconds
def format_time(seconds: float) -> str:
    '''Formats time in seconds to a human-readable string.'''
    minutes = seconds // 60
    seconds %= 60
    return f"{minutes:.0f} minutes {seconds:.2f} seconds"

# Function for sending requests to API and returning JSON response data
def fetch_data(url: str, headers: typing.Dict) -> typing.Dict:
    '''Sends a GET request to the API and returns JSON response data.'''
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP error responses
        return response.json()  # Return dictionary from response formatted in JSON
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
        return {}  # Return an empty dictionary in case of an error

# User data processing function
def process_user_data(headers: typing.Dict, user: typing.Dict):
    '''Processes user data, fetching and storing manager's and devices' information.'''
    user['cost_center'] = user['onPremisesExtensionAttributes']['extensionAttribute15']
    del user['onPremisesExtensionAttributes']

    # Fetch manager info directly here
    manager_url = f"{API_BASE_URL}/users/{user['id']}/manager?$select=displayName,mail"
    manager_response = requests.get(manager_url, headers=headers)
    
    if manager_response.status_code == 200:
        manager_data = manager_response.json()
        user['manager_name'] = manager_data['displayName']
        user['manager_mail'] = manager_data['mail']
    elif manager_response.status_code == 404:
        logging.warning(f"User {user['displayName']} does not have a manager.")
        user['manager_name'] = None
        user['manager_mail'] = None
    else:
        logging.error(f"Request error: {manager_response.status_code}")
        return

    # Fetch devices info directly here
    devices_url = f"{API_BASE_URL}/users/{user['id']}/ownedDevices?$select=displayName,id,enrollmentType,operatingSystem,isManaged,approximateLastSignInDateTime,manufacturer,model"
    devices_data = fetch_data(devices_url, headers)
    user['devices'] = devices_data['value']

# User data grabbing function
def get_users_from_API(headers: typing.Dict) -> typing.Dict:
    '''Retrieves user data from the API based on specified criteria.'''
    start = time.time()
    all_users = []

    next_link = f"{API_BASE_URL}/users?$count=true&$filter=onPremisesExtensionAttributes/extensionAttribute11+eq+'Employee'+and+accountEnabled+eq+true&$select=id,displayName,mail,jobTitle,officeLocation,department,onPremisesExtensionAttributes"

    while next_link:
        json_data = fetch_data(next_link, headers=headers)
        all_users += json_data['value']
        next_link = json_data.get('@odata.nextLink')

    user_count = len(all_users)

    logging.info(f"Today we have {user_count} users")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for user in all_users:
            if user.get('id'):
                futures.append(executor.submit(
                    process_user_data, headers, user))
        for future in concurrent.futures.as_completed(futures):
            pass

    end = time.time()
    logging.info(f"Data grabbing completed! {user_count}")
    elapsed_time = (end - start)
    logging.info(f"Grabbing process took {format_time(elapsed_time)}")
    return all_users

# Function to get users from affected pilot groups
def get_affected_users(headers: typing.Dict) -> typing.Dict:
    '''Retrieves members data from affected pilot groups.'''
    all_users = []
    for naming_tag in PILOT_GROUPS_NAMING_TAGS:
        next_link = f"{API_BASE_URL}/groups?filter=startsWith(displayName,'{naming_tag}')&$expand=members"

        while next_link:
            json_data = fetch_data(next_link, headers=headers)
            all_users += json_data['value']
            next_link = json_data.get('@odata.nextLink')
    return all_users
