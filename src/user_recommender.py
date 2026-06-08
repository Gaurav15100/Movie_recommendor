from collections import Counter

from src.preference_engine import PreferenceEngine


class UserRecommender:

    def __init__(self, hybrid_recommender):
        self.hybrid_recommender = hybrid_recommender
        
        self.preference_engine = (
            PreferenceEngine(
                hybrid_recommender
            )
        )

    def get_recommendations(
        self,
        user_ratings,
        top_n=10
    ):

        all_recommendations = []

        for movie, rating in user_ratings.items():

            if rating >= 4:

                recs = (
                    self.hybrid_recommender
                    .get_recommendations(
                        movie,
                        top_n=10
                    )
                )

                for title in recs["title"]:

                    all_recommendations.extend(
                        [title] * rating
                    )

        counts = Counter(
            all_recommendations
        )
        
        profile = (
            self.preference_engine
            .build_profile(
                user_ratings
            )
        )

        for movie in user_ratings:

            counts.pop(
                movie,
                None
            )
        
        for movie in list(counts.keys()):

            movie_row = (
                self.hybrid_recommender.movies[
                    self.hybrid_recommender.movies[
                        "title"
                    ] == movie
                ]
            )

            if movie_row.empty:
                continue

            genres = (
                movie_row.iloc[0]["genres"]
            )

            bonus = (
                self.preference_engine
                .score_movie(
                    genres,
                    profile
                )
            )

            counts[movie] += bonus

        return counts.most_common(
            top_n
        )