import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient
import certifi


def create_app():
    app = Flask(__name__)
    # Set up mongodb client
    # Added certifi snippet
    client = MongoClient("mongodb+srv://superUser:HurleyShark1441|@initflask.yjeyivn.mongodb.net/test",
                         tlsCAFile=certifi.where())
    app.db = client.Microblog

    @app.route('/', methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]

        return render_template("home.html", entries=entries_with_date)

    return app
