# app.py
from flask import Flask, render_template, session
from models import db
from routes.routes import routes
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "SESSION_SECRET"

db.init_app(app)
app.register_blueprint(routes)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
