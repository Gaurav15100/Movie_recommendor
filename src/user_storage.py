import json
from pathlib import Path


class UserStorage:

    def __init__(self, username):

        self.filepath = (
            Path("data/users")
            / f"{username}.json"
        )

    def load_ratings(self):

        if not self.filepath.exists():
            return {}

        with open(
            self.filepath,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def save_ratings(
        self,
        ratings
    ):

        with open(
            self.filepath,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                ratings,
                file,
                indent=4
            )

    def add_rating(
        self,
        movie,
        rating
    ):

        ratings = self.load_ratings()

        ratings[movie] = rating

        self.save_ratings(
            ratings
        )
        
    def delete_rating(
        self,
        movie
    ):

        ratings = self.load_ratings()

        if movie in ratings:

            del ratings[movie]

            self.save_ratings(
                ratings
            )