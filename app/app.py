import sys
import os

from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.tmdb_service import TMDBService

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
tmdb = TMDBService(TMDB_API_KEY)

import streamlit as st
from src.hybrid_recommender import HybridRecommender

st.title("CineMatch")
st.caption(
    "Hybrid Movie Recommendation System "
    "(Content-Based + Collaborative Filtering)"
)

recommender = HybridRecommender(
    "data/raw/movies.csv",
    "data/raw/tags.csv",
    "data/raw/ratings.csv"
)

movie_title = st.selectbox(
    "Search or select a movie",
    sorted(recommender.movies["title"].tolist()),
    index=None,
    placeholder="Start typing a movie name..."
)

if movie_title and st.button("Get Recommendations"):
    recommendations = recommender.get_recommendations(
        movie_title
    )

    st.subheader("Recommended For You")

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
                    f"Release Date: "
                    f"{movie_data['release_date']}"
                )
                
            if movie_data.get("vote_average"):
                st.write(
                    f"TMDB Rating: "
                    f"{movie_data['vote_average']:.1f}/10"
                )

            if movie_data.get("overview"):
                st.write(
                    movie_data["overview"]
                )
    
    cols = st.columns(3)

    for idx, (_, row) in enumerate(
        recommendations.iterrows()
    ):

        with cols[idx % 3]:

            rec_title = row["title"].split("(")[0].strip()

            rec_movie = tmdb.search_movie(
                rec_title
            )

            if rec_movie:

                poster_url = tmdb.get_poster_url(
                    rec_movie.get("poster_path")
                )

                if poster_url:
                    st.image(
                        poster_url,
                        width=250
                    )

                st.markdown(
                    f"**{row['title']}**"
                )

                rating = round(
                    rec_movie.get("vote_average", 0),
                    1
                )

                st.write(f"⭐ {rating}/10")

                st.caption(
                    row["genres"]
                )
    
    #st.dataframe(
    #    recommendations,
    #    hide_index=True,
     #   use_container_width=True
    #)
    
    