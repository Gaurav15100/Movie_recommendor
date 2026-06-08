import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.hybrid_recommender import HybridRecommender
from src.user_recommender import UserRecommender

hybrid = HybridRecommender(
    "data/raw/movies.csv",
    "data/raw/tags.csv",
    "data/raw/ratings.csv"
)

user = UserRecommender(hybrid)

ratings = {
    "Toy Story (1995)": 5,
    "Jurassic Park (1993)": 4,
    "Forrest Gump (1994)": 5
}

print(
    user.get_recommendations(ratings)
)