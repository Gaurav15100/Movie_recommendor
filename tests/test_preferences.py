import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.hybrid_recommender import HybridRecommender
from src.preference_engine import PreferenceEngine

recommender = HybridRecommender(
    "data/raw/movies.csv",
    "data/raw/tags.csv",
    "data/raw/ratings.csv"
)

engine = PreferenceEngine(
    recommender
)

from src.user_storage import UserStorage

storage = UserStorage(
    "gaurav"
)

ratings = storage.load_ratings()

profile = engine.build_profile(
    ratings
)

print(profile)