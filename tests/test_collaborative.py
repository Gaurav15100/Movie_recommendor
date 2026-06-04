import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.collaborative_recommender import (
    CollaborativeRecommender
)

recommender = CollaborativeRecommender(
    "data/raw/ratings.csv",
    "data/raw/movies.csv"
)

print(
    recommender.get_recommendations(1)
)