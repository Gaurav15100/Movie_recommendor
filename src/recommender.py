import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:
    def __init__(self, movies_path, tags_path):
        self.movies = pd.read_csv(movies_path)
        tags = pd.read_csv(tags_path)
        
        movie_tags = (
            tags.groupby("movieId")["tag"]
            .apply(lambda x: " ".join(sorted(set(x.astype(str)))))
            .reset_index()
        )

        self.movies = self.movies.merge(
            movie_tags,
            on="movieId",
            how="left"
        )

        self.movies["tag"] = self.movies["tag"].fillna("")

        self.movies["features"] = (
            self.movies["genres"].str.replace("|", " ", regex=False)
            + " "
            + self.movies["tag"]
        )

        self.tfidf = TfidfVectorizer()
        self.tfidf_matrix = self.tfidf.fit_transform(
            self.movies["features"]
        )

        self.cosine_sim = cosine_similarity(self.tfidf_matrix)

        self.indices = pd.Series(
            self.movies.index,
            index=self.movies["title"]
        ).drop_duplicates()

        self.title_to_movieid = pd.Series(
            self.movies["movieId"].values,
            index=self.movies["title"]
        ).drop_duplicates()

    def get_recommendations(self, title, top_n=10):
        idx = self.indices[title]

        sim_scores = list(enumerate(self.cosine_sim[idx]))

        sim_scores = sorted(
            sim_scores,
            key=lambda x: x[1],
            reverse=True
        )

        sim_scores = [
            score
            for score in sim_scores
            if score[0] != idx
        ]

        sim_scores = sim_scores[:top_n]

        movie_indices = [i[0] for i in sim_scores]

        recommended_movies = self.movies.iloc[movie_indices].copy()
        
        recommended_movies["genres"] = (
        recommended_movies["genres"]
        .str.replace("|", ", ", regex=False)
    )

        recommended_movies["similarity_score"] = [
            round(score, 3) for _, score in sim_scores
        ]

        return recommended_movies[
            ["title", "genres", "similarity_score"]
        ]