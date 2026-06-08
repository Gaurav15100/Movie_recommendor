import sys
import os

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

import streamlit as st

from src.tmdb_service import TMDBService
from src.hybrid_recommender import HybridRecommender
from src.user_storage import UserStorage


TMDB_API_KEY = os.getenv("TMDB_API_KEY")
tmdb = TMDBService(TMDB_API_KEY)

st.title("⭐ Rate Movies")

username = st.text_input(
    "Username",
    value="gaurav"
)

storage = UserStorage(username)

recommender = HybridRecommender(
    "data/raw/movies.csv",
    "data/raw/tags.csv",
    "data/raw/ratings.csv"
)

movie_title = st.selectbox(
    "Search Movie",
    sorted(recommender.movies["title"].tolist())
)

clean_title = movie_title.split("(")[0].strip()

movie_data = tmdb.search_movie(
    clean_title
)

if movie_data:

    col1, col2 = st.columns([1, 3])

    with col1:

        poster_url = tmdb.get_poster_url(
            movie_data.get("poster_path")
        )

        if poster_url:
            st.image(
                poster_url,
                use_container_width=True
            )

    with col2:

        st.subheader(movie_data["title"])

        if movie_data.get("release_date"):
            st.write(
                f"Release Date: {movie_data['release_date']}"
            )

        if movie_data.get("vote_average"):
            st.write(
                f"TMDB Rating: {movie_data['vote_average']:.1f}/10"
            )

        if movie_data.get("overview"):
            st.write(
                movie_data["overview"]
            )

rating = st.slider(
    "Your Rating",
    1,
    5,
    5
)

if st.button("Save Rating"):

    storage.add_rating(
        movie_title,
        rating
    )

    st.success(
        f"Saved rating for {movie_title}"
    )