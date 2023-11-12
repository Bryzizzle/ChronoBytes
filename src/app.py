from flask import Flask, render_template
from os import getenv
from api.inrix import InrixAPI
from api.yelp import YelpAPI

from utils import polygons

INRIX_APPID = getenv('INRIX_APPID')
INRIX_TOKEN = getenv('INRIX_TOKEN')
YELP_APIKEY = getenv('YELP_APIKEY')
print(INRIX_APPID, INRIX_TOKEN, YELP_APIKEY)

inrix = InrixAPI(INRIX_APPID, INRIX_TOKEN)
yelp = YelpAPI(YELP_APIKEY)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process/<string:request>/<int:start_time>/<int:duration>/<float(signed=True):loc_lat>/<float("
           "signed=True):loc_long>")
def process(request: str, start_time: int, duration: int, loc_lat: float, loc_long: float):
    # Retrieve and process the drive time polygons from the INRIX API
    dt_polygons_xml = inrix.get_drivetime_polygons(loc_lat, loc_long, "D", duration).text
    dt_polygons_coords = polygons.get_polygon_coordinates(dt_polygons_xml)

    # Get the furthest radius from the polygons (in km) and cap it at Yelp's 40 KM limit
    dt_radius = polygons.furthest_distance((loc_lat, loc_long), dt_polygons_coords)
    dt_radius = int(min(40000, dt_radius * 1000))

    # Query the Yelp API for restaurants within the allocated radius
    yelp_response = yelp.parsed_business_search(loc_lat, loc_long, dt_radius, limit=50)

    # Cull all the restaurants outside the initial polygon
    yelp_culled = polygons.in_polygon(yelp_response, dt_polygons_coords)

    # print(yelp_culled)

    ret = ""
    for business in yelp_culled:
        ret += business.generate_llm_string()
        ret += "<br/>"

    return ret

