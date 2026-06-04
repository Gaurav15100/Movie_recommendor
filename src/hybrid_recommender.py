import pandas as pd

from src.recommender import MovieRecommender
from src.collaborative_recommender import (
    CollaborativeRecommender
)


class HybridRecommender:

    def __init__(
        self,
        movies_path,
        tags_path,
        ratings_path
    ):

        self.content_recommender = (
            MovieRecommender(
                movies_path,
                tags_path
            )
        )

        self.collaborative_recommender = (
            CollaborativeRecommender(
                ratings_path,
                movies_path
            )
        )
        
        self.movies = (
            self.content_recommender.movies
        )

    def get_recommendations(
        self,
        title,
        top_n=10
    ):

        content_recs = (
            self.content_recommender
            .get_recommendations(
                title,
                top_n=5
            )
        )
        
        content_recs["source"] = "Content"

        movie_id = (
            self.content_recommender
            .title_to_movieid[title]
        )

        try:

            collaborative_recs = (
                self.collaborative_recommender
                .get_recommendations(
                    movie_id,
                    top_n=5
                )
            )
            
            collaborative_recs["source"] = "Collaborative"

        except ValueError:

            collaborative_recs = (
                content_recs.iloc[0:0]
            )

        hybrid_recs = pd.concat(
            [content_recs, collaborative_recs],
            ignore_index=True
        ).drop_duplicates(
            subset=["title"]
        )

        return hybrid_recs[
            [
                "title",
                "genres",
                "similarity_score",
                "source"
            ]
        ].head(top_n)