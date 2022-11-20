from flask import Flask, request, send_from_directory

from .mask2face import generate_face

app = Flask(__name__)


@app.route("/")
def index():
    return send_from_directory("./static", "index.html")


@app.route("/<path:name>")
def download_file(name):
    return send_from_directory("./static", name)


@app.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        img_binary = request.files["picture"]
        res = generate_face(img_binary)

        return res
