import array
import datetime


class Device:
    def __init__(self, id: str, name: str, group: str, os: str, type: str, last_checkin_date: datetime):
        self._id = id
        self._name = name
        self._group = group
        self._os = os
        self._type = type
        self._last_checkin_date = last_checkin_date

    @property
    def id(self) -> str:
        return self._id

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
    def type(self) -> str:
        return self._type

    @property
    def last_checkin_date(self) -> datetime:
        return self._last_checkin_date


class User:
    def __init__(
            self,
            id: str,
            name: str,
            mail: str,
            manager_name: str,
            manager_mail: str,
            job_title: str,
            location: str,
            device_list: list[Device]
    ):
        self._id = id
        self._name = name
        self._mail = mail
        self._manager_name = manager_name
        self._manager_mail = manager_mail
        self._job_title = job_title
        self._location = location
        self._device_list = device_list

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def mail(self) -> str:
        return self._mail

    @property
    def manager_name(self) -> str:
        return self._manager_name

    @property
    def manager_mail(self) -> str:
        return self._manager_mail

    @property
    def job_title(self) -> str:
        return self._job_title

    @property
    def location(self) -> str:
        return self._location

    @property
    def device_list(self) -> list[Device]:
        return self._device_list

    def add_device(self, device: Device):
        self._device_list.append(device)


class Department:
    def __init__(self, name: str, cost_center: int, user_list: list[User]):
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
    def user_list(self) -> list[User]:
        return self._user_list

    def add_user(self, user: User):
        self._user_list.append(user)
