# import libraries
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    # get name parameter
    name = request.args.get("name")

    # greet with name
    return f"Hello {name}"

if __name__ == "__main__":
    app.run(debug=True)