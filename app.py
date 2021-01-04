from oso import Oso
from polar import Variable

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    oso = Oso()
    oso.load_file("hello.polar")

    name = "fred"

    return render_template("app.html", name=name)