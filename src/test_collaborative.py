from collaborative_recommender import (
    CollaborativeRecommender
)

recommender = CollaborativeRecommender(
    "data/raw/ratings.csv",
    "data/raw/movies.csv"
)

print(
    recommender.get_recommendations(1)
)