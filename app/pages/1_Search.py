import sys
import os

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.tmdb_service import TMDBService
from src.hybrid_recommender import HybridRecommender
from src.user_storage import UserStorage
from src.preference_engine import PreferenceEngine

import streamlit as st

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
tmdb = TMDBService(TMDB_API_KEY)

st.title("🔍 Search Movies")

recommender = HybridRecommender(
    "data/raw/movies.csv",
    "data/raw/tags.csv",
    "data/raw/ratings.csv"
)

storage = UserStorage(
    "gaurav"
)

preference_engine = (
    PreferenceEngine(
        recommender
    )
)

search_type = st.radio(
    "Search Type",
    [
        "Movie",
        "Genre"
    ]
)

if search_type == "Movie":

    movie_title = st.selectbox(
        "Search or select a movie",
        sorted(
            recommender.movies["title"].tolist()
        ),
        index=None,
        placeholder="Start typing a movie name..."
    )

else:

    genres = sorted(
        set(
            genre
            for movie_genres in recommender.movies["genres"]
            for genre in movie_genres.split("|")
        )
    )

    selected_genres = st.multiselect(
        "Select Genres",
        genres
    )

    if selected_genres:

        genre_movies = recommender.movies.copy()

        for genre in selected_genres:

            genre_movies = genre_movies[
                genre_movies["genres"]
                .str.contains(
                    genre,
                    regex=False
                )
            ]

        genre_movies = genre_movies.sort_values(
            "title"
        )

        st.subheader(
            f"{', '.join(selected_genres)} Movies"
        )

        cols = st.columns(3)

        for idx, (_, row) in enumerate(
            genre_movies.head(12).iterrows()
        ):

            with cols[idx % 3]:

                movie_name = (
                    row["title"]
                    .split("(")[0]
                    .strip()
                )

                movie_data = tmdb.search_movie(
                    movie_name
                )

                if movie_data:

                    poster_url = tmdb.get_poster_url(
                        movie_data.get(
                            "poster_path"
                        )
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
                        movie_data.get(
                            "vote_average",
                            0
                        ),
                        1
                    )

                    st.write(
                        f"⭐ {rating}/10"
                    )

                    st.caption(
                        row["genres"]
                    )
                    
if (
    search_type == "Movie"
    and movie_title
    and st.button(
        "Get Recommendations"
    )
):
    recommendations = recommender.get_recommendations(
        movie_title
    )
    
    ratings = storage.load_ratings()

    profile = (
        preference_engine
        .build_profile(
            ratings
        )
    )
    
    recommendations[
        "preference_score"
    ] = recommendations[
        "genres"
    ].apply(
        lambda genres:
        preference_engine.score_movie(
            genres.replace(
                ", ",
                "|"
            ),
            profile
        )
    )
    
    recommendations = (
        recommendations
        .sort_values(
            "preference_score",
            ascending=False
        )
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
                
