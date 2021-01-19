import json

from flask import Flask, render_template
import sqlite3

from werkzeug.exceptions import HTTPException

app = Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/list', methods=['GET'])
def list_users():
    con = sqlite3.connect("users.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM users")

    rows = cur.fetchall()
    return render_template("list.html", rows=rows)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


if __name__ == '__main__':
    app.run(debug=True, port=55555)
