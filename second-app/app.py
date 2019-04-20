# import libraries
from flask import Flask, request, render_template, abort, session, redirect, url_for, flash
import pandas as pd
from datetime import datetime

# initiate flask app
app = Flask(__name__)

# set a secret key
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# home page
@app.route("/", methods=["GET", "POST"])
def index():
    # handle get requets
    if request.method == "GET":
        # if there's an active session get username and posts attributed to user
        if "username" in session:
            username = session["username"]
            statuses_db = pd.read_csv("statuses.csv")
            # retrieve statuses and turn to dict to be accessed by jinja
            statuses = statuses_db[statuses_db["author"] == username].to_dict("records")
        else:
            username = None
            statuses = None
        return render_template(
            "index.html", 
            title="Homepage", 
            username=username, 
            statuses=statuses
        )

    # handle post requests
    if request.method == "POST":
        # get the posted update
        status_update = request.form.get("status_update")

        # validation
        if not status_update:
            abort(404, description="No update was written")
        else:
            # store in the database
            statuses_db = pd.read_csv("statuses.csv")
            statuses_db = statuses_db.append({
                "author": session["username"],
                "message": status_update,
                "time": datetime.now()
            }, ignore_index=True)
            statuses_db.to_csv("statuses.csv")
        
        return redirect(url_for("index"))


# register page
@app.route("/register", methods=["GET", "POST"])
def register():
    # import credentials database
    cred_db = pd.read_csv("./credentials.csv")
    
    # handle get requests
    if request.method  == "GET":
        return render_template("register.html", title="Register")

    # handle post requests
    elif request.method == "POST":
        # get the username and password that were just entered
        username = request.form.get("username")
        password = request.form.get("password")

        # validation before storing credentials
        if not username and not password:
            abort(404, description="No username and password were provided")

        elif username in cred_db["username"].tolist():
            abort(404, description="This username already exists")
        
        else:
            cred_db = cred_db.append({
                "username": username,
                "password": password
            }, ignore_index=True)
            cred_db.to_csv("credentials.csv", index=False)

        flash("You've successfully created an account!")
        return render_template("success.html", title="Successful Registration",
                               credentials={"username": username, "password": password})

# login page
@app.route("/login", methods=["GET", "POST"])
def login():
    # import credentials database
    cred_db = pd.read_csv("./credentials.csv")

    # handle get
    if request.method == "GET":
        return render_template("login.html", title="Login")

    # handle post
    elif request.method == "POST":
        # get the username and password that were entered in
        username = request.form.get("username")
        password = request.form.get("password")

        # get the user's password from the database
        user_pass = cred_db[cred_db["username"] == username]["password"].item()

        # validate and proceed
        if not username or not password:
            abort(404, description="A username and/or password weren't provided")

        elif username not in cred_db["username"].to_list():
            abort(404, description="The username does not exist")

        elif password != user_pass:
            abort(404, description="The password is incorrect")

        else:
            session["username"] = username
            return redirect(url_for("index"))

# logout clear session
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)