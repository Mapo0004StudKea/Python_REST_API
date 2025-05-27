# anime.py
import requests

def fetch_anime_data(title):
    url = f"https://api.jikan.moe/v4/anime?q={title}&limit=1"
    response = requests.get(url)
    data = response.json()

    if "data" in data and len(data["data"]) > 0:
        anime = data["data"][0]
        return {
            "mal_id": anime["mal_id"],
            "title": anime["title"],
            "year": anime["year"] or "Unknown",
            "genre": ", ".join([g["name"] for g in anime.get("genres", [])]),
            "plot": anime.get("synopsis", "No synopsis available."),
            "director": "N/A (Anime)"
        }
    else:
        return None
