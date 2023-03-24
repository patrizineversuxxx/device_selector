import random
import openpyxl
from Data import *
from Parser import *


def check_department_target(department):
    return int(0.12 * len(department.user_list))+1


path = r'C:\KEK\ID_RANDOM.xlsx'
workbook = openpyxl.load_workbook(path)
spreadsheet = workbook.active

department_list = {}
user_list = {}
device_list = []
target_percent = 0.12
parse_datatable(spreadsheet, department_list, user_list, device_list)

selected_users = []
selected_device_list = []
