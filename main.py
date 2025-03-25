import flask


# TODO: change this to your academic email
AUTHOR = "lumbroso@seas.upenn.edu"


app = flask.Flask(__name__)


# This is a simple route to test your server


@app.route("/")
def hello():
    return f"Hello from my Password Validator! &mdash; <tt>{AUTHOR}</tt>"


# This is a sample "password validator" endpoint
# It is not yet implemented, and will return HTTP 501 in all situations


@app.route("/v1/checkPassword", methods=["POST"])
def check_password():
    data = flask.request.get_json() or {}
    pw = data.get("password", "")
    if len(pw) < 8:
        return flask.jsonify({"valid": False, "reason": "Length must be >= 8"}), 400
    uppercase_count = sum(1 for c in pw if c.isupper())
    if uppercase_count < 2:
        return flask.jsonify({"valid": False, "reason": "Needs at least 2 uppercase letters"}), 400
    digit_count = sum(1 for c in pw if c.isdigit())
    if digit_count < 2:
        return flask.jsonify({"valid": False, "reason": "Needs at least 2 digits"}), 400
    special_count = sum(1 for c in pw if c in "!@#$%^&*")
    if special_count < 1:
        return flask.jsonify({"valid": False, "reason": "Needs at least 1 special character"}), 400

    # FIXME: to be implemented
    return flask.jsonify({"valid": True, "reason": "Good password!"}), 200
