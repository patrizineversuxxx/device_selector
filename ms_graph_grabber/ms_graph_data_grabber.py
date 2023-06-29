import time
import requests
import concurrent.futures
from file_recorder.json_parser import *


def invoke_cost_center(user: typing.Dict):
    user['cost_center'] = user.get("onPremisesExtensionAttributes").get("extensionAttribute15")
    del user['onPremisesExtensionAttributes']

def fetch_manager_info(headers: typing.Dict, user: typing.Dict):
    manager_url = r'https://graph.microsoft.com/beta/users/' + \
                user['id']+r'/manager?$select=displayName,mail'

    manager_response = requests.get(manager_url, headers=headers)
    manager_data = manager_response.json()

    user['manager_name'] = manager_data.get("displayName")
    user['manager_mail'] = manager_data.get("mail")

def fetch_devices_info(headers: typing.Dict, user: typing.Dict):
    devices_url = r'https://graph.microsoft.com/beta/users/' + \
                user['id']+r'/ownedDevices?$select=displayName,id,enrollmentType,operatingSystem,' + \
                r'isManaged,approximateLastSignInDateTime,manufacturer,model'

    devices_response = requests.get(devices_url, headers=headers)
    devices_data = devices_response.json()

    user['devices'] = devices_data.get("value")

def process_user_data(headers: typing.Dict, user: typing.Dict):
    fetch_manager_info(headers, user)
    fetch_devices_info(headers, user)
    
def get_users_from_API(headers: typing.Dict) -> typing.Dict:
    start = time.time()
    all_users = []
    
    next_link = r"https://graph.microsoft.com/beta/users?$count=true&$filter=onPremisesExtensionAttributes/extensionAttribute11+eq+'Employee'+and+accountEnabled+eq+true&$select=id,displayName,mail,jobTitle,officeLocation,department,onPremisesExtensionAttributes"
    
    while next_link:
        response = requests.get(next_link, headers=headers)
        json_data = response.json()
        all_users += json_data["value"]
        next_link = json_data.get("@odata.nextLink")

    counter = 0
    user_count = len(all_users)

    print("Today we have ", user_count, "users")
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for user in all_users:
            if user.get('id'):            
                invoke_cost_center(user)
                futures.append(executor.submit(process_user_data, headers, user))
        for future in concurrent.futures.as_completed(futures):
            pass



    end = time.time()
    print("Data grabbing completed!", user_count)
    print("Grabbing process took ", end-start)
    print(start)
    print(end)
    return all_users


def get_intune_devices_from_API(headers: typing.Dict, naming_tags: typing.Dict) -> typing.Dict:
    all_devices = []

    for naming_tag in naming_tags:
        next_link = r"https://graph.microsoft.com/beta/deviceManagement/managedDevices?$filter=startswith(devicename,'"+naming_tag + \
            r"')&select=devicename,userid,azureActiveDirectoryDeviceId,deviceEnrollmentType,operatingSystem,usersLoggedOn"

        while next_link:
            response = requests.get(next_link, headers=headers)
            json_data = response.json()
            all_devices += json_data['value']
            next_link = json_data.get("@odata.nextLink")

    return all_devices
