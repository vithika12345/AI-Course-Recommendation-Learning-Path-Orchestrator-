"""
Verification script to test CourseRecommenderEngine and MultiAgentOrchestrator.
"""

import sys
import os

# Add workspace to path
workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if workspace_dir not in sys.path:
    sys.path.insert(0, workspace_dir)

from engine.recommender import CourseRecommenderEngine
from orchestrator.orchestrator import MultiAgentOrchestrator
from engine.metrics import precision_at_k, recall_at_k, mean_reciprocal_rank, ndcg_at_k


def test_recommender():
    print("--- Testing CourseRecommenderEngine ---")
    engine = CourseRecommenderEngine()
    print(f"Loaded {len(engine.df)} courses successfully.")
    
    results = engine.search_courses(query="Machine Learning Deep Learning PyTorch", top_k=3)
    print(f"Retrieved {len(results)} recommendations.")
    for r in results:
        print(f"  [{r['course_id']}] {r['title']} | Score: {r['match_percentage']}% | Rating: {r['rating']}")
    assert len(results) == 3, "Expected 3 courses"
    print("CourseRecommenderEngine test PASSED!\n")


def test_orchestrator():
    print("--- Testing MultiAgentOrchestrator (Offline Mode) ---")
    orchestrator = MultiAgentOrchestrator(provider="offline")
    
    res = orchestrator.run_pipeline(
        user_query="I want to learn modern machine learning and build neural networks",
        experience_level="Beginner",
        target_role="AI & Machine Learning Engineer",
        hours_per_week=12,
        preferred_learning_style="Hands-on Project Oriented",
        budget_preference="All (Free & Paid)",
        top_k=4
    )
    
    print("Pipeline Execution Completed!")
    print(f"Total Pipeline Latency: {res['metrics']['total_pipeline_latency_s']}s")
    print(f"Target Role: {res['profile']['target_role']}")
    print(f"Skill Gaps: {res['profile']['skill_gaps']}")
    print(f"Courses Found: {len(res['courses'])}")
    print(f"Roadmap Phases: {len(res['roadmap']['phases'])}")
    print(f"Critic Feasibility Score: {res['critique']['feasibility_score']}%")
    print("Trace Steps:")
    for step in res["trace"]:
        print(f"  - {step['agent']}: {step['action']} ({step['duration_seconds']}s)")
        
    assert len(res["courses"]) > 0, "No courses returned"
    assert "phases" in res["roadmap"], "No roadmap phases"
    print("MultiAgentOrchestrator test PASSED!\n")


def test_metrics():
    print("--- Testing Evaluation Metrics ---")
    rec = ["C001", "C002", "C005", "C010", "C015"]
    truth = ["C001", "C002", "C015", "C016"]
    
    p5 = precision_at_k(rec, truth, k=5)
    r5 = recall_at_k(rec, truth, k=5)
    mrr = mean_reciprocal_rank(rec, truth)
    ndcg = ndcg_at_k(rec, truth, k=5)
    
    print(f"Precision@5: {p5}")
    print(f"Recall@5: {r5}")
    print(f"MRR: {mrr}")
    print(f"NDCG@5: {ndcg}")
    assert p5 > 0 and r5 > 0 and mrr == 1.0, "Metrics test failed"
    print("Metrics test PASSED!\n")


if __name__ == "__main__":
    test_recommender()
    test_orchestrator()
    test_metrics()
    print("ALL TESTS PASSED SUCCESSFULLY!")
