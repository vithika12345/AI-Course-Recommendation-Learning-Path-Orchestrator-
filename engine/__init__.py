"""
Engine module initialization.
"""

from .recommender import CourseRecommenderEngine
from .metrics import precision_at_k, recall_at_k, mean_reciprocal_rank, ndcg_at_k

__all__ = [
    "CourseRecommenderEngine",
    "precision_at_k",
    "recall_at_k",
    "mean_reciprocal_rank",
    "ndcg_at_k"
]
