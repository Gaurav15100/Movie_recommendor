import requests


class TMDBService:

    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self, api_key):
        self.api_key = api_key

    def search_movie(self, title):

        url = f"{self.BASE_URL}/search/movie"

        params = {
            "api_key": self.api_key,
            "query": title
        }

        response = requests.get(
            url,
            params=params
        )

        response.raise_for_status()

        results = response.json()["results"]

        if not results:
            return None

        return results[0]

    def get_poster_url(self, poster_path):

        if not poster_path:
            return None

        return (
            f"https://image.tmdb.org/t/p/w500"
            f"{poster_path}"
        )