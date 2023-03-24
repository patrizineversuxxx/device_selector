import array
import datetime


class Device:
    def __init__(self, name: str, group: str, os: str, last_checkin_date: datetime):
        self._name = name
        self._group = group
        self._os = os
        self._last_checkin_date = last_checkin_date

    @property
    def name(self) -> str:
        return self._name

    @property
    def group(self) -> str:
        return self._group

    @property
    def os(self) -> str:
        return self._os

    @property
    def last_checkin_date(self) -> datetime:
        return self._last_checkin_date


class User:
    def __init__(self, name: str, manager: str, job_title: str, location: str, device_list: array):
        self._name = name
        self._manager = manager
        self._job_title = job_title
        self._location = location
        self._device_list = device_list

    @property
    def name(self) -> str:
        return self._name

    @property
    def manager(self) -> str:
        return self._manager

    @property
    def job_title(self) -> str:
        return self._job_title

    @property
    def location(self) -> str:
        return self._location

    @property
    def device_list(self) -> array:
        return self._device_list

    def add_device(self, device: Device):
        self._device_list.append(device)


class Department:
    def __init__(self, name: str, cost_center: int, user_list: array):
        self._name = name
        self._cost_center = cost_center
        self._user_list = user_list

    @property
    def name(self) -> str:
        return self._name

    @property
    def cost_center(self) -> int:
        return self._cost_center

    @property
    def user_list(self) -> array:
        return self._user_list

    def add_user(self, user: User):
        self._user_list.append(user)