import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.user_storage import UserStorage

user = UserStorage(
    "gaurav"
)

user.add_rating(
    "Toy Story (1995)",
    5
)

print(
    user.load_ratings()
)