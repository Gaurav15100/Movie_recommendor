import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from dotenv import load_dotenv
import os

from src.tmdb_service import TMDBService

load_dotenv()

api_key = os.getenv("TMDB_API_KEY")

tmdb = TMDBService(api_key)

movie = tmdb.search_movie(
    "Toy Story"
)

print(movie["title"])
print(movie["release_date"])
print(movie["overview"][:200])
print(
    tmdb.get_poster_url(
        movie["poster_path"]
    )
)