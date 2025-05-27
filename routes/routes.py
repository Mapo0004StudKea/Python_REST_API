# routes.py
from flask import Blueprint, request, jsonify
from models import db, Movie
from omdb import fetch_movie_data
from anime import fetch_anime_data

routes = Blueprint('routes', __name__)

@routes.route("/api/search", methods=["POST"])
def search_media():
    data = request.get_json()
    title = data.get("title")
    media_type = data.get("type")  # "movie" eller "anime"

    if media_type == "movie":
        existing = Movie.query.filter_by(title=title, source_type="movie").first()
        if existing:
            return jsonify({"message": "Movie already exists"}), 409
        result = fetch_movie_data(title)
        if not result:
            return jsonify({"error": "Movie not found"}), 404
        result["source_type"] = "movie"
        movie = Movie(**result)

    elif media_type == "anime":
        existing = Movie.query.filter_by(title=title, source_type="anime").first()
        if existing:
            return jsonify({"message": "Anime already exists"}), 409
        result = fetch_anime_data(title)
        if not result:
            return jsonify({"error": "Anime not found"}), 404
        result["source_type"] = "anime"
        movie = Movie(**result)

    else:
        return jsonify({"error": "Invalid type"}), 400

    db.session.add(movie)
    db.session.commit()
    return jsonify({"message": f"{media_type.capitalize()} added", "data": result}), 201

@routes.route("/api/movies", methods=["GET"])
def get_movies():
    movies = Movie.query.all()
    return jsonify([{
        "id": m.id,
        "title": m.title,
        "year": m.year,
        "genre": m.genre,
        "plot": m.plot,
        "favorite": m.is_favorite
    } for m in movies])

@routes.route("/api/movies/<int:id>/favorite", methods=["PATCH"])
def toggle_favorite(id):
    movie = Movie.query.get_or_404(id)
    movie.is_favorite = not movie.is_favorite
    db.session.commit()
    return jsonify({"message": "Favorite toggled", "favorite": movie.is_favorite})

@routes.route("/api/movies/<int:id>/review", methods=["PATCH"])
def update_review(id):
    movie = Movie.query.get_or_404(id)
    data = request.get_json()
    movie.user_review = data.get("review", "")
    db.session.commit()
    return jsonify({"message": "Review updated", "review": movie.user_review})


@routes.route("/api/movies/<int:id>", methods=["DELETE"])
def delete_movie(id):
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    return jsonify({"message": "Media deleted"})
