"""
Multi-Agent Orchestrator
Coordinates sequential agent execution flow, aggregates shared context,
measures execution latencies, and produces a complete explainable trace.
"""

import time
from typing import Dict, Any, List, Optional, Callable
from engine.recommender import CourseRecommenderEngine
from agents.profiler_agent import ProfilerAgent
from agents.retrieval_agent import RetrievalAgent
from agents.path_planner_agent import PathPlannerAgent
from agents.critic_agent import CriticAgent


class MultiAgentOrchestrator:
    """
    Central Controller for the Course Recommendation Multi-Agent System.
    Orchestrates:
    1. ProfilerAgent -> Deconstructs learner intent & gaps
    2. RetrievalAgent -> Searches & ranks hybrid course candidates
    3. PathPlannerAgent -> Assembles structured weekly curriculum
    4. CriticAgent -> Audits pedagogical rigor & cognitive load
    """

    def __init__(
        self,
        engine: Optional[CourseRecommenderEngine] = None,
        provider: str = "offline",
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.engine = engine or CourseRecommenderEngine()
        self.provider = provider
        self.api_key = api_key
        self.model = model
        self._init_agents()

    def _init_agents(self):
        self.profiler = ProfilerAgent(provider=self.provider, api_key=self.api_key, model=self.model)
        self.retrieval = RetrievalAgent(engine=self.engine, provider=self.provider, api_key=self.api_key, model=self.model)
        self.planner = PathPlannerAgent(provider=self.provider, api_key=self.api_key, model=self.model)
        self.critic = CriticAgent(provider=self.provider, api_key=self.api_key, model=self.model)

    def update_configuration(
        self,
        provider: str,
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ):
        """Allows dynamic switching of LLM backend during runtime."""
        self.provider = provider
        self.api_key = api_key
        self.model = model
        self._init_agents()

    def run_pipeline(
        self,
        user_query: str,
        experience_level: str = "Beginner",
        target_role: str = "Machine Learning Engineer",
        hours_per_week: int = 10,
        preferred_learning_style: str = "Hands-on Project Oriented",
        budget_preference: str = "All (Free & Paid)",
        preferred_category: Optional[str] = None,
        top_k: int = 4,
        status_callback: Optional[Callable[[str], None]] = None
    ) -> Dict[str, Any]:
        """
        Executes the 4-stage multi-agent orchestration pipeline.
        """
        total_start = time.time()
        trace: List[Dict[str, Any]] = []

        def log_step(agent_name: str, action: str, details: str, duration: float):
            trace.append({
                "timestamp": round(time.time() - total_start, 2),
                "agent": agent_name,
                "action": action,
                "details": details,
                "duration_seconds": round(duration, 3)
            })
            if status_callback:
                status_callback(f"[{agent_name}] {action} completed in {round(duration, 2)}s")

        # Step 1: Profiler Agent
        if status_callback:
            status_callback("[ProfilerAgent] Analyzing learner background, goals, and skill gaps...")
        s1_start = time.time()
        profile = self.profiler.analyze_profile(
            user_query=user_query,
            experience_level=experience_level,
            target_role=target_role,
            hours_per_week=hours_per_week,
            preferred_learning_style=preferred_learning_style,
            budget_preference=budget_preference
        )
        s1_dur = time.time() - s1_start
        log_step(
            agent_name="ProfilerAgent",
            action="Diagnosed Learner Profile",
            details=f"Identified target: {profile.get('target_role')}, Gaps: {', '.join(profile.get('skill_gaps', [])[:3])}",
            duration=s1_dur
        )

        # Step 2: Retrieval Agent
        if status_callback:
            status_callback("[RetrievalAgent] Executing hybrid vector & metadata search on course catalog...")
        s2_start = time.time()
        free_only = "Free Only" in budget_preference
        retrieval_res = self.retrieval.retrieve_and_rank(
            profile=profile,
            top_k=top_k,
            free_only=free_only,
            preferred_category=preferred_category
        )
        courses = retrieval_res["courses"]
        s2_dur = time.time() - s2_start
        log_step(
            agent_name="RetrievalAgent",
            action="Hybrid Course Retrieval",
            details=f"Retrieved {len(courses)} candidate courses using query: '{retrieval_res.get('query_used')}'",
            duration=s2_dur
        )

        # Step 3: Path Planner Agent
        if status_callback:
            status_callback("[PathPlannerAgent] Assembling sequenced weekly learning trajectory...")
        s3_start = time.time()
        roadmap = self.planner.plan_roadmap(profile=profile, courses=courses)
        s3_dur = time.time() - s3_start
        log_step(
            agent_name="PathPlannerAgent",
            action="Curriculum Path Synthesis",
            details=f"Created {roadmap.get('total_estimated_weeks', 12)}-week roadmap spanning {len(roadmap.get('phases', []))} phases",
            duration=s3_dur
        )

        # Step 4: Critic Agent
        if status_callback:
            status_callback("[CriticAgent] Performing pedagogical review & feasibility audit...")
        s4_start = time.time()
        critique = self.critic.review_plan(profile=profile, courses=courses, roadmap=roadmap)
        s4_dur = time.time() - s4_start
        log_step(
            agent_name="CriticAgent",
            action="Pedagogical Quality Audit",
            details=f"Audited curriculum. Feasibility Score: {critique.get('feasibility_score')}% ({critique.get('workload_status')})",
            duration=s4_dur
        )

        total_elapsed = round(time.time() - total_start, 2)

        return {
            "success": True,
            "profile": profile,
            "courses": courses,
            "roadmap": roadmap,
            "critique": critique,
            "trace": trace,
            "metrics": {
                "total_pipeline_latency_s": total_elapsed,
                "courses_evaluated": len(self.engine.df),
                "courses_recommended": len(courses),
                "provider_mode": self.provider.title(),
                "model": self.model or "heuristic-offline"
            }
        }
