from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "<p>Hello, World!</p>"


@app.route("/process/<string:request>/<int:start_time>/<int:duration>/<int:loc_lat>/<int:loc_lon>")
def process():
    pass


