"""
Recommendation System Evaluation Metrics
Implements standard academic IR & Recommender metrics:
- Precision@K
- Recall@K
- Mean Reciprocal Rank (MRR)
- Normalized Discounted Cumulative Gain (NDCG@K)
"""

import math
from typing import List, Any


def precision_at_k(recommended: List[Any], ground_truth: List[Any], k: int = 5) -> float:
    """Calculates Precision@K: relevant items among top K recommendations / K."""
    if k <= 0:
        return 0.0
    rec_k = recommended[:k]
    relevant_hits = len(set(rec_k).intersection(set(ground_truth)))
    return round(relevant_hits / k, 4)


def recall_at_k(recommended: List[Any], ground_truth: List[Any], k: int = 5) -> float:
    """Calculates Recall@K: relevant items among top K recommendations / total relevant."""
    if not ground_truth:
        return 0.0
    rec_k = recommended[:k]
    relevant_hits = len(set(rec_k).intersection(set(ground_truth)))
    return round(relevant_hits / len(ground_truth), 4)


def mean_reciprocal_rank(recommended: List[Any], ground_truth: List[Any]) -> float:
    """Calculates Reciprocal Rank of the first relevant item in recommendations."""
    for rank, item in enumerate(recommended, start=1):
        if item in ground_truth:
            return round(1.0 / rank, 4)
    return 0.0


def ndcg_at_k(recommended: List[Any], ground_truth: List[Any], k: int = 5) -> float:
    """Calculates Normalized Discounted Cumulative Gain at K (binary relevance)."""
    if k <= 0 or not ground_truth:
        return 0.0

    dcg = 0.0
    for i, item in enumerate(recommended[:k]):
        rel = 1.0 if item in ground_truth else 0.0
        dcg += (2.0 ** rel - 1.0) / math.log2(i + 2)

    # Ideal DCG: top min(len(ground_truth), k) are all relevant
    idcg = 0.0
    ideal_items_count = min(len(ground_truth), k)
    for i in range(ideal_items_count):
        idcg += (2.0 ** 1.0 - 1.0) / math.log2(i + 2)

    if idcg == 0.0:
        return 0.0
    return round(dcg / idcg, 4)


def benchmark_sample_queries() -> dict:
    """
    Runs a representative benchmark over sample user personas
    to produce empirical results for the Project Report and Viva.
    """
    # Test personas and synthetic relevant courses based on domain expertise
    personas = [
        {
            "query": "Deep learning natural language processing transformers PyTorch",
            "relevant": ["C002", "C007", "C015", "C016", "C017"]
        },
        {
            "query": "Full stack web development React Node.js JavaScript Next.js",
            "relevant": ["C005", "C006", "C013", "C014", "C048", "C080"]
        },
        {
            "query": "DevOps cloud architecture Kubernetes Docker AWS CI/CD",
            "relevant": ["C010", "C011", "C012", "C045", "C046", "C047"]
        },
        {
            "query": "Cybersecurity ethical hacking penetration testing network security",
            "relevant": ["C020", "C021", "C022", "C059", "C060"]
        }
    ]
    return personas
