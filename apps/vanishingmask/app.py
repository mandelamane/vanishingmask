from flask import Flask, render_template, request

from .mask2face import generate_face

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        img_binary = request.files["picture"]
        res = generate_face(img_binary)

        return res
