import time
import requests
import concurrent.futures
import typing


PILOT_GROUPS_NAMING_TAGS = ("POC", "UAT", "_test_vneskorodov", "pilot")
API_BASE_URL = "https://graph.microsoft.com/beta"


def format_time(seconds: float) -> str:
    minutes = seconds // 60
    seconds %= 60
    return f"{minutes:.0f} minutes {seconds:.2f} seconds"


def fetch_data(url: str, headers: typing.Dict) -> typing.Dict:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP error responses
    return response.json()


# Data processing functions
def process_user_data(headers: typing.Dict, user: typing.Dict):
    user['cost_center'] = user.get(
        "onPremisesExtensionAttributes").get("extensionAttribute15")
    del user['onPremisesExtensionAttributes']

    # Fetch manager info directly here
    manager_url = f"{API_BASE_URL}/users/{user['id']}/manager?$select=displayName,mail"
    manager_data = fetch_data(manager_url, headers)
    user['manager_name'] = manager_data.get('displayName')
    user['manager_mail'] = manager_data.get('mail')

    # Fetch devices info directly here
    devices_url = f"{API_BASE_URL}/users/{user['id']}/ownedDevices?$select=displayName,id,enrollmentType,operatingSystem,isManaged,approximateLastSignInDateTime,manufacturer,model"
    devices_data = fetch_data(devices_url, headers)
    user['devices'] = devices_data.get('value')


def get_users_from_API(headers: typing.Dict) -> typing.Dict:
    start = time.time()
    all_users = []

    next_link = f"{API_BASE_URL}/users?$count=true&$filter=onPremisesExtensionAttributes/extensionAttribute11+eq+'Employee'+and+accountEnabled+eq+true&$select=id,displayName,mail,jobTitle,officeLocation,department,onPremisesExtensionAttributes"

    while next_link:
        response = requests.get(next_link, headers=headers)
        json_data = response.json()
        all_users += json_data['value']
        next_link = json_data.get('@odata.nextLink')

    user_count = len(all_users)

    print("Today we have ", user_count, "users")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for user in all_users:
            if user.get('id'):
                futures.append(executor.submit(
                    process_user_data, headers, user))
        for future in concurrent.futures.as_completed(futures):
            pass

    end = time.time()
    print("Data grabbing completed!", user_count)
    elapsed_time = (end - start)
    print("Grabbing process took", format_time(elapsed_time))
    print(start)
    print(end)
    return all_users


def get_affected_users(headers: typing.Dict) -> typing.Dict:
    all_users = []
    for naming_tag in PILOT_GROUPS_NAMING_TAGS:
        next_link = f"{API_BASE_URL}/groups?filter=startsWith(displayName,'{naming_tag}')&$expand=members"

        while next_link:
            response = requests.get(next_link, headers=headers)
            json_data = response.json()
            all_users += json_data['value']
            next_link = json_data.get('@odata.nextLink')

    return all_users
