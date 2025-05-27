# omdb.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

def fetch_movie_data(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data.get("Response") == "True":
        return {
            "imdb_id": data["imdbID"],
            "title": data["Title"],
            "year": data["Year"],
            "genre": data["Genre"],
            "plot": data["Plot"],
            "director": data["Director"]
        }
    else:
        return None
