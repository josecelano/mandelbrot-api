import os
import sys

from waitress import serve
from flask import Flask, render_template, redirect
from src.mandelbrot_api.mandelbrot import MandelbrotController
from src.mandelbrot_api.orbit import OrbitController

OUTPUT_DIRECTORY = "./output/"

if not os.path.exists(OUTPUT_DIRECTORY):
    os.makedirs(OUTPUT_DIRECTORY)

api = Flask(__name__)


@api.route('/')
def home_redirect():
    return redirect("/api", code=302)


@api.route("/api")
def entry_point():
    """Entry point for API."""
    return render_template("index.html")


@api.route("/api/tiles", methods=['GET'])
def tile_index():
    """Download a tile."""
    return MandelbrotController.invoke(OUTPUT_DIRECTORY)


@api.route("/api/ascii-graphs", methods=['GET'])
def ascii_graph_index():
    """Download a ascii graph."""
    return MandelbrotController.invoke(OUTPUT_DIRECTORY)


@api.route("/api/orbits", methods=['GET'])
def orbit_index():
    """Download a orbit graph."""
    return OrbitController.invoke(OUTPUT_DIRECTORY)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'dev':
        # Development
        api.run(debug=True, host='0.0.0.0', port=5000)
    else:
        # Production
        serve(api, host="0.0.0.0", port=80)
