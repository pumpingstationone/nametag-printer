from asgiref.wsgi import WsgiToAsgi
from flask import Flask, render_template, request

from .logconf import setup_logging
from .printer import print_name

setup_logging()

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        second_line = request.form["second_line"]

        print_name(name, second_line)

        return render_template("printing.html")

    return render_template("index.html")


# Create ASGI app for compatibility with Uvicorn
asgi_app = WsgiToAsgi(app)

if __name__ == "__main__":
    app.run(debug=True)
