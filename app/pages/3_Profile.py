import sys

from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

import streamlit as st

from src.user_storage import UserStorage


st.title("👤 Profile")

username = st.text_input(
    "Username",
    value="gaurav"
)

storage = UserStorage(
    username
)

ratings = storage.load_ratings()

if not ratings:

    st.info(
        "No ratings found."
    )

else:

    st.subheader(
        "Movies Rated"
    )

    st.write(
        f"Total Ratings: {len(ratings)}"
    )

    for movie, rating in sorted(
        ratings.items()
    ):

        col1, col2 = st.columns(
            [5, 1]
        )

        with col1:

            st.write(
                f"⭐ {rating}/5 — {movie}"
            )

        with col2:

            if st.button(
                "Delete",
                key=movie
            ):

                storage.delete_rating(
                    movie
                )

                st.rerun()

        st.write("")