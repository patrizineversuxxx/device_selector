import typing


class Config:
    def __init__(self, redirect_uri: str, client_credentials: str, client_id: str, authority_url: str, scopes: list[str], file_paths: typing.Dict[str, str]):
        self._redirect_uri = redirect_uri
        self._client_credentials = client_credentials
        self._client_id = client_id
        self._authority_url = authority_url
        self._scopes = scopes
        self._file_paths = file_paths

    @property
    def redirect_uri(self) -> str:
        return self._redirect_uri
    
    @property
    def client_credentials(self) -> str:
        return self._client_credentials
    
    @property
    def client_id(self) -> str:
        return self._client_id
    
    @property
    def authority_url(self) -> str:
        return self._authority_url
    
    @property
    def scopes(self) -> list:
        return self._scopes
    
    @property
    def file_paths(self) -> typing.Dict[str,str]:
        return self._file_paths


"""


    "naming_tags": [
        "EVN",
        "MOW"
    ],
    "office_locations": [
        "AM+Yerevan",
        "RU+Moscow",
        "RU+Novosibirsk"
    ],
    "target_percent": 0.12,
    "minimal_target": 45,
    "minimal_selected_group" : "AAD_Joined",
    "required" : {"AAD_Joined":15, "Hybrid_Joined":30, "macOS":15}"""