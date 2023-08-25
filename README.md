# Device selector - app for canary testing of software updates using information from Microsoft services
Backend prototype created with Python and MSAL library

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This project was created for purposes of canary testing software updates or group policy changes. Before everything will be applied to all employees, 
it must be tested  on different users from each department. This tool gets information from Microsoft Gparh API, 
provides each device a certain device tag, based on operating system and enrollment type, and selects needed device count from certain device group.
Project contains two main parts - schedule based data grabbing from MS Graph API and device selection based on grabbed data.

## Technologies
Project is created with:
* Python version: 3.10.11
* MSAL library  version: 1.21.0
* Openpyxl library version: 3.1.1
* Schedule library version: 1.2.0

## Setup
For using this product, you need to have:

* Azure Active Directory license
* Administrator rights to create app registration and grant admin permissions to the app
* Python 3.10
* Installed libraries from requirments.txt

After cloning the repository, you should create folder for configurational files. Later you need to create these files:

* config.json - file, where tenant connection information will be stored
* file_paths.json - file, where are file paths to intermediate and result files on your local device
* selection_conditions.json - file, where selection conditions will be stored

Later you need to create connection to your Azure tenant using this guideline.

Right now, my application, which works with Graph API, uses daemon app flow. It creates connection token silently and uses application delegated permissions:

* Device.Read.All
* DeviceManagementManagedDevices
* Directory.Read.All
* User.ReadBasic.All

For creating connection to Microsoft services, you need to put several parameters to your config.json file:

* "client_id" - your app registration id in Azure Active Directory
* "scope" - for daemon apps "https://graph.microsoft.com/.default"
* "thumbprint" - after creating certificate in app registration, copy and paste thumbprint value
* "private_key_file" - path to private key file
* "thumbprint" - after creating certificate in app registration, copy and paste thumbprint value
