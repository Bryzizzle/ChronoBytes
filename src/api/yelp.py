import requests
from dataclasses import dataclass

@dataclass
class YelpBusiness:
    id: str
    alias: str
    name: str
    image_url: str
    url: str
    review_count: int
    rating: float
    coord_lat: float
    coord_long: float
    price: int
    disp_location: str
    disp_phone: str
    distance: float

    categories: list[str]

    def __init__(self, raw_data: dict):
        self.id = raw_data["id"]
        self.alias = raw_data["alias"]
        self.name = raw_data["name"]
        self.image_url = raw_data["image_url"]
        self.url = raw_data["url"]
        self.review_count = raw_data["review_count"]
        self.rating = raw_data["rating"]

        self.coord_lat = raw_data["coordinates"]["latitude"]
        self.coord_long = raw_data["coordinates"]["longitude"]

        try:
            self.price = len(raw_data["price"])
        except KeyError:
            # Do an average priced restaurant if no rating is given
            self.price = 2

        self.disp_location = " ".join(raw_data["location"]["display_address"])
        self.disp_phone = raw_data["display_phone"]
        self.distance = raw_data["distance"]

        categories = raw_data.get("categories", {})
        self.categories = [category["title"] for category in categories]

    def get_location_point(self):
        return self.coord_lat, self.coord_long

    def generate_llm_string(self):
        return f" - {self.id} | {self.name} | {self.rating}/5 | {', '.join(self.categories)}"


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

    def parsed_business_search(self, lat: float, long: float, radius: int, term=None, categories=None, price=None,
                               open_at=None, attributes=None, sort_by=None, limit=20, offset=0):
        api_data = self.business_search(lat, long, radius, term, categories, price, open_at, attributes, sort_by,
                                        limit, offset).json()

        ret_list = []

        for business in api_data["businesses"]:
            ret_list.append(YelpBusiness(business))

        return ret_list
