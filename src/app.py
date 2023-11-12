from flask import Flask
from os import getenv
from api.inrix import InrixAPI
from api.yelp import YelpAPI

INRIX_APPID = os.getenv('INRIX_APPID')
INRIX_TOKEN = os.getenv('INRIX_TOKEN')
YELP_APIKEY = os.getenv('YELP_APIKEY')
print(INRIX_APPID, INRIX_TOKEN, YELP_APIKEY)



app = Flask(__name__)


@app.route("/")
def index():
    return "<p>Hello, World!</p>"


@app.route("/process/<string:request>/<int:start_time>/<int:duration>/<int:loc_lat>/<int:loc_lon>")

def process():

    req = request
    # chat gpt to parse req

    # location and time into inrix
    inrix = InrixAPI()


    pass


