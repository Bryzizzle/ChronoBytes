from flask import Flask, render_template
from os import getenv
from api.inrix import InrixAPI
from api.yelp import YelpAPI
from api.chatgpt import make_yelp_query

from utils import polygons

INRIX_APPID = getenv('INRIX_APPID')
INRIX_TOKEN = getenv('INRIX_TOKEN')
YELP_APIKEY = getenv('YELP_APIKEY')
print(INRIX_APPID, INRIX_TOKEN, YELP_APIKEY)

inrix = InrixAPI(INRIX_APPID, INRIX_TOKEN)
yelp = YelpAPI(YELP_APIKEY)

app = Flask(__name__)

center = []


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

    # Parse the user query to yelp-readable parameters
    llm_term, llm_categories, llm_price = make_yelp_query(request)

    # Query the Yelp API for restaurants within the allocated radius
    yelp_response = yelp.parsed_business_search(loc_lat, loc_long, dt_radius, llm_term, llm_categories, llm_price,
                                                limit=50)

    # Cull all the restaurants outside the initial polygon
    yelp_culled = polygons.in_polygon(yelp_response, dt_polygons_coords)

    print(yelp_culled)

    ret = ""
    for business in yelp_culled:
        ret += business.generate_llm_string()
        ret += "<br/>"

    return ret



@app.route('/submit', methods=['POST'])
def submit():
    # Handle form submission here
    query = request.form.get('query')
    duration = request.form.get('duration')
    print(query, duration)
    list_of_courses = [query, duration, center[0], center[1]]
    return render_template("result.html", courses=list_of_courses) 

# link submit to process to result

@app.route('/coord')
def coord():
    return render_template('coordinates.html')

@app.route('/get_location', methods=['POST'])
def get_location():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    center.append(latitude)
    center.append(longitude)

    # Here, you can process the latitude and longitude as needed
    location_info = f'Latitude {latitude} Longitude {longitude}'

    return location_info

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/get_route')
def get_route():
    # Sample route coordinates
    route_coordinates = [
        {'lat': 37.7749, 'lng': -122.4194},
        {'lat': 34.0522, 'lng': -118.2437},
        # Add more coordinates as needed
    ]

    return jsonify({'route': route_coordinates})