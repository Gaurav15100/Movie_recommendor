import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.hybrid_recommender import HybridRecommender


recommender = HybridRecommender(
    "data/raw/movies.csv",
    "data/raw/tags.csv",
    "data/raw/ratings.csv"
)

print(
    recommender.get_recommendations(
        "Toy Story (1995)"
    )
)