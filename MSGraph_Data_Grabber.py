import msal
import webbrowser
import requests
import json
from Data import *


def read_config():
    f = open("config.json")
    params = json.load(f)
    return params


def save_json(all_entities, path):
    with open(path, "w") as file:
        json.dump(all_entities, file)


def user_to_json_grabbing(headers, path):
    all_users = []

    office_locations = ['AM+Yerevan', 'RU+Moscow', 'RU+Novosibirsk']

    for office_location in office_locations:
        next_link = r'https://graph.microsoft.com/v1.0/users?$search="officeLocation:' + office_location + \
            r'"&$filter=accountEnabled+eq+true&$select=id,displayname,mail,jobtitle,department,officeLocation,accountEnabled'

        while next_link:
            response = requests.get(next_link, headers=headers)
            json_data = response.json()
            all_users += json_data["value"]
            next_link = json_data.get("@odata.nextLink")

    for user in all_users:
        if user.get('id'):
            manager_url = f'https://graph.microsoft.com/v1.0/users/{user["id"]}/manager?$select=mail'
            manager_response = requests.get(manager_url, headers=headers)
            manager_data = manager_response.json()
            user['manager'] = manager_data.get('mail')

    save_json(all_entities=all_users, path=path)


def device_to_json_grabbing(headers, path):
    all_devices = []

    naming_tags = params['naming_tags']
    for naming_tag in naming_tags:
        next_link = r"https://graph.microsoft.com/beta/deviceManagement/managedDevices?$filter=startswith(devicename,'"+naming_tag + \
            "')&select=id,devicename,userid,azureActiveDirectoryDeviceId,deviceEnrollmentType,operatingSystem,usersLoggedOn"

        while next_link:
            response = requests.get(next_link, headers=headers)
            json_data = response.json()
            all_devices += json_data["value"]
            next_link = json_data.get("@odata.nextLink")

    save_json(all_entities=all_devices, path=path)


def connect_to_api(params):  # needed to rewrite to user auth flow

    id = params['client_id']
    sec = params['client_secrets']
    authority_url = params['authority_url']

    scopes = ['User.Read', 'User.ReadBasic.All', 'Device.Read',
              'DeviceManagementManagedDevices.Read.All', 'Directory.Read.All']

    app = msal.PublicClientApplication(
        id,
        authority=authority_url
    )

    flow = app.initiate_device_flow(scopes=scopes)
    print(flow)
    app_flow = flow['message']
    webbrowser.open(flow['verification_uri'])

    token = app.acquire_token_by_device_flow(flow)

    access_token_id = token['access_token']
    headers = {'Authorization': 'Bearer ' +
               access_token_id, 'ConsistencyLevel': 'eventual'}


#r"https://graph.microsoft.com/beta/deviceManagement/managedDevices?$filter=(startswith(devicename, 'EVN')+or+startswith(devicename,'MOW'))&select=devicename"
# user_to_json_grabbing(headers=headers)
# device_to_json_grabbing(headers=headers)
params = read_config()
# Opening JSON file


# Closing file
f.close()

print('DONE!')
