import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class CollaborativeRecommender:

    def __init__(
        self,
        ratings_path,
        movies_path,
        min_ratings=10
    ):

        self.ratings = pd.read_csv(ratings_path)
        self.movies = pd.read_csv(movies_path)

        movie_rating_counts = (
            self.ratings.groupby("movieId")["rating"]
            .count()
        )

        popular_movies = movie_rating_counts[
            movie_rating_counts >= min_ratings
        ]

        self.filtered_ratings = self.ratings[
            self.ratings["movieId"].isin(
                popular_movies.index
            )
        ]

        self.movie_user_matrix = (
            self.filtered_ratings.pivot_table(
                index="movieId",
                columns="userId",
                values="rating"
            )
        )

        self.movie_similarity = cosine_similarity(
            self.movie_user_matrix.fillna(0)
        )

        self.movie_lookup = (
            self.movies.set_index("movieId")
        )

    def get_recommendations(
        self,
        movie_id,
        top_n=10
    ):

        if movie_id not in self.movie_user_matrix.index:
            raise ValueError(
                f"Movie ID {movie_id} not found "
                f"in collaborative dataset."
            )

        idx = self.movie_user_matrix.index.get_loc(
            movie_id
        )

        sim_scores = list(
            enumerate(
                self.movie_similarity[idx]
            )
        )

        sim_scores = sorted(
            sim_scores,
            key=lambda x: x[1],
            reverse=True
        )

        sim_scores = [
            score
            for score in sim_scores
            if self.movie_user_matrix.index[
                score[0]
            ] != movie_id
        ]

        sim_scores = sim_scores[:top_n]

        recommended_movie_ids = [
            self.movie_user_matrix.index[i[0]]
            for i in sim_scores
        ]

        recommendations = (
            self.movie_lookup.loc[
                recommended_movie_ids
            ]
            .copy()
        )

        recommendations["genres"] = (
            recommendations["genres"]
            .str.replace(
                "|",
                ", ",
                regex=False
            )
        )

        recommendations["similarity_score"] = [
            round(score, 3)
            for _, score in sim_scores
        ]

        return recommendations[
            [
                "title",
                "genres",
                "similarity_score"
            ]
        ]