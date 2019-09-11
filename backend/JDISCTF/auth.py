from flask import (
    request,
    Blueprint
)

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        return "This isn't supported yet."
    else:
        return "This should return a login page."