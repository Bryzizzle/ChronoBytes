import requests

from functools import cache


class InrixAPI:
    api_url: str

    appid: str
    hash_token: str
    access_token: str

    def __init__(self, appid: str, hash_token: str, api_url: str = "https://api.iq.inrix.com"):
        self.appid = appid
        self.hash_token = hash_token

        self.api_url = api_url

        self.update_token()

    def update_token(self):
        self.access_token = self.get("auth/v1/appToken", {
            "appId": self.appid,
            "hashToken": self.hash_token
        }, use_auth=False).json()["result"]["token"]

    @cache
    def get_drivetime_polygons(self, lat, long, range_type=None, duration=None, datetime=None, criteria=None):
        param = {
            "center": f"{lat}|{long}"
        }

        if range_type is not None:
            param["rangeType"] = range_type

        if duration is not None:
            param["duration"] = duration

        if datetime is not None:
            param["dateTime"] = datetime

        if criteria is not None:
            param["criteria"] = criteria

        print(param)

        return self.get("drivetimePolygons", param)

    def get(self, endpoint: str, queries: dict[str, str] = {}, headers: dict[str, str] = {}, use_auth: bool = True):
        # Generate the URL to call
        call_url = f"{self.api_url}/{endpoint}"

        # Add authentication to the header
        if use_auth:
            headers["Authorization"] = f"Bearer {self.access_token}"

        print(requests.Request("GET", call_url, params=queries, headers=headers).prepare().url)

        return requests.get(call_url, params=queries, headers=headers)
