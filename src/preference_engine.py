class PreferenceEngine:

    def __init__(
        self,
        recommender
    ):

        self.recommender = recommender

    def build_profile(
        self,
        ratings
    ):

        genre_scores = {}

        for movie, rating in ratings.items():

            if rating < 4:
                continue

            movie_row = (
                self.recommender.movies[
                    self.recommender.movies[
                        "title"
                    ] == movie
                ]
            )

            if movie_row.empty:
                continue

            genres = (
                movie_row.iloc[0]["genres"]
                .split("|")
            )

            for genre in genres:

                genre_scores[
                    genre
                ] = (
                    genre_scores.get(
                        genre,
                        0
                    )
                    + rating
                )

        return genre_scores

    def score_movie(
        self,
        genres,
        profile
    ):

        score = 0

        for genre in genres.split("|"):

            score += profile.get(
                genre,
                0
            )

        return score