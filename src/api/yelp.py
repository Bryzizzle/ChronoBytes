import requests


class YelpAPI:
    api_url: str
    api_key: str

    def __init__(self, api_key: str, api_url: str = "https://api.yelp.com/v3"):
        self.api_key = api_key
        self.api_url = api_url

    def get(self, endpoint: str, queries: dict[str, str] = {}, headers: dict[str, str] = {}, use_auth: bool = True):
        # Generate the URL to call
        call_url = f"{self.api_url}/{endpoint}"

        # Add authentication to the header
        if use_auth:
            headers["Authorization"] = f"Bearer {self.api_key}"

        print(requests.Request("GET", call_url, params=queries, headers=headers).prepare().url)

        return requests.get(call_url, params=queries, headers=headers)

    def business_search(self, lat: float, long: float, radius: int, term=None, categories=None, price=None,
                        open_at=None, attributes=None, sort_by=None, limit=20, offset=0):
        param = {
            "latitude": lat,
            "longitude": long,
            "radius": radius,
            "limit": limit,
            "offset": offset
        }

        if term is not None:
            param["term"] = term

        if categories is not None:
            param["categories"] = categories

        if price is not None:
            param["price"] = price

        if open_at is not None:
            param["open_at"] = open_at

        if attributes is not None:
            param["attributes"] = attributes

        if sort_by is not None:
            param["sort_by"] = sort_by

        print(param)

        return self.get("businesses/search", param)
