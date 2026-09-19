"""
Retrieval Agent
Queries the Hybrid Course Recommender Engine with parameters formulated by
the Profiler Agent and annotates matches with pedagogical justifications.
"""

from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
from engine.recommender import CourseRecommenderEngine


class RetrievalAgent(BaseAgent):
    def __init__(
        self,
        engine: CourseRecommenderEngine,
        provider: str = "offline",
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ):
        super().__init__(
            name="RetrievalAgent",
            role="Curriculum Retrieval & Search Specialist",
            provider=provider,
            api_key=api_key,
            model=model
        )
        self.engine = engine

    def retrieve_and_rank(
        self,
        profile: Dict[str, Any],
        top_k: int = 4,
        free_only: bool = False,
        preferred_category: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes hybrid course search and generates contextual rationale.
        """
        keywords = profile.get("search_keywords", [])
        query_str = " ".join(keywords) if isinstance(keywords, list) else str(keywords)
        target_level = profile.get("current_level", "Beginner")

        # Query the hybrid recommendation engine
        raw_courses = self.engine.search_courses(
            query=query_str,
            target_level=target_level,
            preferred_category=preferred_category,
            free_only=free_only,
            top_k=top_k
        )

        annotated_courses = []
        for course in raw_courses:
            # Generate justification for why this course fits the user
            rationale = self._generate_course_rationale(course, profile)
            course_copy = dict(course)
            course_copy["why_recommended"] = rationale
            annotated_courses.append(course_copy)

        return {
            "courses": annotated_courses,
            "query_used": query_str,
            "target_level": target_level,
            "count": len(annotated_courses),
            "_meta": {
                "agent": self.name,
                "role": self.role,
                "provider": self.provider.title(),
                "model": self.model
            }
        }

    def _generate_course_rationale(self, course: Dict[str, Any], profile: Dict[str, Any]) -> str:
        """
        Synthesizes a short, punchy reason why this course directly serves the learner.
        """
        title = course.get("title", "")
        skills = ", ".join(course.get("skills_covered", [])[:3])
        level = course.get("level", "All")
        target_role = profile.get("target_role", "your career goal")

        return (
            f"Directly addresses critical competency in {skills}. "
            f"Its {level.lower()} difficulty level provides the optimal learning curve towards {target_role}."
        )
