import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

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

    st.subheader(f"Top Recommendations for: {movie_title}")
    
    st.dataframe(
        recommendations,
        hide_index=True,
        use_container_width=True
    )
    
    