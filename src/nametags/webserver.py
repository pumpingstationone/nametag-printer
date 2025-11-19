from .printer import print_name
from flask import Flask, request, render_template
from asgiref.wsgi import WsgiToAsgi

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        print_name(name)

        return render_template("printing.html")

    return render_template("index.html")


# Create ASGI app for compatibility with Uvicorn
asgi_app = WsgiToAsgi(app)

if __name__ == "__main__":
    app.run(debug=True)
