from recommender import MovieRecommender

recommender = MovieRecommender(
    "data/raw/movies.csv",
    "data/raw/tags.csv"
)

recommendations = recommender.get_recommendations(
    "Toy Story (1995)"
)

print(recommendations)