# CineMatch

## Overview
CineMatch is a hybrid movie recommendation system combining Content-Based Filtering and Collaborative Filtering to produce personalized movie suggestions.

## Features
- Content-based recommendations using movie genres and tags (TF-IDF + cosine similarity).
- Collaborative recommendations based on user ratings (item-item similarity).
- Hybrid mode that merges content and collaborative candidates.
- Simple Streamlit UI for interactive exploration.

## Technologies Used
- Python 3.8+
- pandas
- scikit-learn
- Streamlit

## Project Structure
- `app/` — Streamlit app (`app.py`)
- `data/raw/` — Raw datasets (`movies.csv`, `ratings.csv`, `tags.csv`, `links.csv`)
- `data/processed/` — (ignored) processed data / artifacts
- `models/` — (ignored) trained models or serialized artifacts
- `notebooks/` — exploration and experiments
- `src/` — core recommender implementations and tests
- `requirements.txt` — Python dependencies
- `README.md` — this file

## Installation Instructions
1. Create and activate a virtual environment:
   - Windows (PowerShell)
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   - macOS / Linux
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run
- Run the Streamlit app:
  ```bash
  streamlit run app/app.py
  ```
- Or run quick local tests:
  ```bash
  python src/test_hybrid.py
  ```

## Explanation: Content-Based Filtering
Content-based filtering builds item profiles from metadata (here: `genres` + `tags`). Text features are vectorized using TF-IDF and item-item similarity is computed via cosine similarity. For a selected movie, the system returns movies with highest cosine similarity on the feature vectors.

## Explanation: Collaborative Filtering
Collaborative filtering uses user ratings to find similarity between items in the user-item rating matrix (item-item approach). After filtering for sufficiently-rated movies, cosine similarity is computed between movie vectors (users as features) to recommend items similar in user-rating patterns.

## Explanation: Hybrid Recommendation System
The hybrid approach merges the strengths of both methods: content-based helps with cold-start items via metadata similarity, and collaborative helps surface items that users with similar tastes liked. This implementation concatenates content and collaborative candidates and deduplicates by title.

## Future Improvements
- Add unit tests and CI (GitHub Actions).
- Use lightweight sample dataset and provide a data download script or instructions.
- Add caching for similarity matrices and lazy loading for large datasets.
- Consider `git-lfs` for large dataset/artifact management.
- Improve UI with pagination, filters, and rating-based personalization.

## Notes on Data
- The repository currently includes `data/raw/` CSVs. Consider excluding large raw datasets from the repo and provide a small sample or a data download script.
