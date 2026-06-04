import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.recommender import MovieRecommender

recommender = MovieRecommender(
    "data/raw/movies.csv",
    "data/raw/tags.csv"
)

recommendations = recommender.get_recommendations(
    "Toy Story (1995)"
)

print(recommendations)