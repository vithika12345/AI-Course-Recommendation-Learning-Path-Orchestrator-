"""
Course Recommendation Engine
Hybrid Content-Based & Metadata Ranking Engine
Combines TF-IDF feature vectorization, cosine similarity, and metadata boosting.
"""

import os
import re
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class CourseRecommenderEngine:
    """
    Hybrid Course Recommendation Engine.
    Uses TF-IDF over course title, skills, category, and description,
    fused with heuristic metadata boosting (difficulty level match, ratings, duration).
    """

    def __init__(self, data_path: Optional[str] = None):
        if data_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_path = os.path.join(base_dir, "data", "courses.csv")
        
        self.data_path = data_path
        self.df = self._load_data()
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.tfidf_matrix = None
        self._build_index()

    def _load_data(self) -> pd.DataFrame:
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Course dataset not found at {self.data_path}")
        df = pd.read_csv(self.data_path)
        # Fill missing values
        df["skills_covered"] = df["skills_covered"].fillna("")
        df["prerequisites"] = df["prerequisites"].fillna("None")
        df["description"] = df["description"].fillna("")
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(4.5)
        df["duration_hours"] = pd.to_numeric(df["duration_hours"], errors="coerce").fillna(30)
        df["price_usd"] = pd.to_numeric(df["price_usd"], errors="coerce").fillna(0.0)
        return df

    def _build_index(self):
        # Create a rich composite text field for semantic indexing
        corpus = (
            self.df["title"].astype(str) + " " +
            self.df["category"].astype(str) + " " +
            self.df["skills_covered"].astype(str).str.replace(";", " ") + " " +
            self.df["description"].astype(str)
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)

    def search_courses(
        self,
        query: str,
        target_level: Optional[str] = None,
        preferred_category: Optional[str] = None,
        max_duration: Optional[int] = None,
        free_only: bool = False,
        top_k: int = 5,
        alpha: float = 0.65,  # Weight for text similarity
        beta: float = 0.20,   # Weight for course rating
        gamma: float = 0.15   # Weight for level alignment
    ) -> List[Dict[str, Any]]:
        """
        Perform hybrid retrieval scoring:
        Score = alpha * cosine_similarity + beta * normalized_rating + gamma * level_match
        """
        if not query or not query.strip():
            query = "machine learning computer science programming"

        clean_query = re.sub(r"[^a-zA-Z0-9\s]", " ", query)
        query_vec = self.vectorizer.transform([clean_query])
        sim_scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        results = []
        for idx, row in self.df.iterrows():
            sim = float(sim_scores[idx])

            # Rating score (normalized 0 to 1 assuming 4.0 - 5.0 band)
            rating = float(row["rating"])
            norm_rating = max(0.0, min(1.0, (rating - 4.0) / 1.0))

            # Level match bonus
            course_level = str(row["level"]).lower()
            level_score = 0.5  # Neutral default
            if target_level:
                target_level_clean = target_level.lower()
                if course_level == target_level_clean:
                    level_score = 1.0
                elif (
                    (target_level_clean == "beginner" and course_level == "intermediate") or
                    (target_level_clean == "advanced" and course_level == "intermediate")
                ):
                    level_score = 0.6
                else:
                    level_score = 0.2

            # Category filter bonus
            category_match = 1.0
            if preferred_category and preferred_category != "All":
                if preferred_category.lower() in str(row["category"]).lower():
                    category_match = 1.2
                else:
                    category_match = 0.7

            # Price constraint
            price = float(row["price_usd"])
            if free_only and price > 0.0:
                continue

            # Duration constraint
            duration = float(row["duration_hours"])
            if max_duration and duration > max_duration:
                # Soft penalty for exceeding duration
                duration_penalty = 0.8
            else:
                duration_penalty = 1.0

            # Composite hybrid score
            base_score = (alpha * sim) + (beta * norm_rating) + (gamma * level_score)
            composite_score = base_score * category_match * duration_penalty

            match_percentage = min(99.0, max(45.0, round(composite_score * 100, 1)))

            results.append({
                "course_id": row["course_id"],
                "title": row["title"],
                "provider": row["provider"],
                "category": row["category"],
                "level": row["level"],
                "rating": rating,
                "duration_hours": int(duration),
                "price_usd": price,
                "is_free": price == 0.0,
                "skills_covered": [s.strip() for s in str(row["skills_covered"]).split(";") if s.strip()],
                "prerequisites": row["prerequisites"],
                "description": row["description"],
                "url": row["url"],
                "similarity_score": round(sim, 4),
                "match_percentage": match_percentage,
                "composite_score": composite_score
            })

        # Sort descending by composite score
        results.sort(key=lambda x: x["composite_score"], reverse=True)
        return results[:top_k]

    def get_categories(self) -> List[str]:
        """Returns sorted unique categories."""
        categories = ["All"] + sorted(self.df["category"].dropna().unique().tolist())
        return categories

    def get_catalog_dataframe(self) -> pd.DataFrame:
        """Returns the full catalog DataFrame."""
        return self.df.copy()
