# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imdb_id = db.Column(db.String(20), unique=True, nullable=True)
    mal_id = db.Column(db.Integer, unique=True, nullable=True)
    title = db.Column(db.String(100))
    year = db.Column(db.String(10))
    genre = db.Column(db.String(100))
    plot = db.Column(db.Text)
    director = db.Column(db.String(100))
    user_review = db.Column(db.Text)
    is_favorite = db.Column(db.Boolean, default=False)
    source_type = db.Column(db.String(20))  # "movie" eller "anime"

