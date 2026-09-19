"""
Path Planner Agent (Curriculum & Learning Path Planner)
Assembles retrieved courses into a sequenced, phased, week-by-week learning roadmap
with concrete milestones and hands-on portfolio projects.
"""

import json
import re
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent


class PathPlannerAgent(BaseAgent):
    def __init__(self, provider: str = "offline", api_key: Optional[str] = None, model: Optional[str] = None):
        super().__init__(
            name="PathPlannerAgent",
            role="Syllabus Architect & Career Roadmap Planner",
            provider=provider,
            api_key=api_key,
            model=model
        )

    def plan_roadmap(
        self,
        profile: Dict[str, Any],
        courses: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Synthesizes a 4-phase structured timeline connecting the recommended courses.
        """
        system_prompt = (
            "You are a master Instructional Designer and Curriculum Architect.\n"
            "Organize the given courses into a sequenced 4-phase learning roadmap.\n"
            "Respond ONLY in valid JSON format with keys:\n"
            "- total_estimated_weeks: int\n"
            "- phases: list of 3-4 objects, each having:\n"
            "    - phase_number: int\n"
            "    - title: string\n"
            "    - weeks: string (e.g. 'Weeks 1-3')\n"
            "    - focus_course_id: string\n"
            "    - focus_course_title: string\n"
            "    - core_skills: list of strings\n"
            "    - milestone_deliverable: string\n"
            "- capstone_project: object with 'title', 'description', 'tech_stack'\n"
            "- certification_recommendation: string\n"
        )

        course_summaries = [
            f"ID: {c.get('course_id')} | Title: {c.get('title')} | Level: {c.get('level')} | Duration: {c.get('duration_hours')} hrs"
            for c in courses
        ]

        user_prompt = (
            f"Learner Target Role: {profile.get('target_role')}\n"
            f"Hours/Week: {profile.get('hours_per_week', 10)}\n"
            f"Identified Gaps: {', '.join(profile.get('skill_gaps', []))}\n"
            f"Available Courses:\n" + "\n".join(course_summaries)
        )

        llm_response = self.call_llm(system_prompt, user_prompt, temperature=0.3)
        raw_text = llm_response["content"]

        try:
            cleaned = re.sub(r"^```json\s*", "", raw_text.strip(), flags=re.MULTILINE)
            cleaned = re.sub(r"^```\s*", "", cleaned.strip(), flags=re.MULTILINE)
            roadmap_data = json.loads(cleaned)
        except Exception:
            roadmap_data = self._heuristic_roadmap(profile, courses)

        roadmap_data["_meta"] = {
            "agent": self.name,
            "role": self.role,
            "duration_s": llm_response["duration_s"],
            "provider": llm_response["provider"],
            "model": llm_response["model"]
        }
        return roadmap_data

    def _heuristic_fallback(
        self,
        system_prompt: str,
        user_prompt: str,
        fallback_reason: Optional[str] = None
    ) -> str:
        # Fallback JSON
        data = {
            "total_estimated_weeks": 12,
            "phases": [
                {
                    "phase_number": 1,
                    "title": "Foundational Prerequisite & Theory Setup",
                    "weeks": "Weeks 1-3",
                    "focus_course_id": "C001",
                    "focus_course_title": "Foundational Core Course",
                    "core_skills": ["Syntax Mastery", "Algorithmic Basics", "Environment Setup"],
                    "milestone_deliverable": "Complete 5 hands-on mini labs and initialize a GitHub repo."
                },
                {
                    "phase_number": 2,
                    "title": "Applied Frameworks & Intermediate Architecture",
                    "weeks": "Weeks 4-7",
                    "focus_course_id": "C002",
                    "focus_course_title": "Intermediate Deep Dive",
                    "core_skills": ["Framework Pipelines", "API Design", "Data Wrangling"],
                    "milestone_deliverable": "Build an end-to-end working service with persistent storage."
                },
                {
                    "phase_number": 3,
                    "title": "Advanced Engineering & Performance Tuning",
                    "weeks": "Weeks 8-10",
                    "focus_course_id": "C010",
                    "focus_course_title": "Production Engineering",
                    "core_skills": ["Deployment", "Docker Containerization", "CI/CD Testing"],
                    "milestone_deliverable": "Containerize your service and deploy a live working prototype."
                },
                {
                    "phase_number": 4,
                    "title": "Comprehensive Capstone & Portfolio Polish",
                    "weeks": "Weeks 11-12",
                    "focus_course_id": "Capstone",
                    "focus_course_title": "Independent Capstone Project",
                    "core_skills": ["Documentation", "System Architecture", "Demo Presentation"],
                    "milestone_deliverable": "Publish complete open-source project with live demo and README."
                }
            ],
            "capstone_project": {
                "title": "Production-Ready Domain Application",
                "description": "Architect an end-to-end industry relevant system addressing a real problem with interactive UI.",
                "tech_stack": ["Python/TypeScript", "Docker", "REST API", "Modern Web Framework"]
            },
            "certification_recommendation": "Target relevant industry credential (e.g. AWS Associate or Coursera Professional Certificate) within 30 days of completion."
        }
        return json.dumps(data, indent=2)

    def _heuristic_roadmap(self, profile: Dict[str, Any], courses: List[Dict[str, Any]]) -> Dict[str, Any]:
        role = profile.get("target_role", "Software Engineer")
        course_list = courses if courses else []

        c1 = course_list[0] if len(course_list) > 0 else {"course_id": "C001", "title": "Core Foundations"}
        c2 = course_list[1] if len(course_list) > 1 else {"course_id": "C002", "title": "Intermediate Architecture"}
        c3 = course_list[2] if len(course_list) > 2 else {"course_id": "C003", "title": "Advanced Specialization"}

        return {
            "total_estimated_weeks": 12,
            "phases": [
                {
                    "phase_number": 1,
                    "title": "Foundational Competencies & Syntax",
                    "weeks": "Weeks 1-3",
                    "focus_course_id": c1.get("course_id", "C001"),
                    "focus_course_title": c1.get("title", "Core Foundations"),
                    "core_skills": c1.get("skills_covered", ["Foundational Theory", "Basics"])[:3],
                    "milestone_deliverable": f"Pass core problem sets and complete starter project for {c1.get('title')}."
                },
                {
                    "phase_number": 2,
                    "title": "Applied Systems & Practical Frameworks",
                    "weeks": "Weeks 4-7",
                    "focus_course_id": c2.get("course_id", "C002"),
                    "focus_course_title": c2.get("title", "Applied Systems"),
                    "core_skills": c2.get("skills_covered", ["Intermediate Tools", "Applied Logic"])[:3],
                    "milestone_deliverable": f"Deploy a functional prototype applying lessons from {c2.get('title')}."
                },
                {
                    "phase_number": 3,
                    "title": "Advanced Topics & Industry Best Practices",
                    "weeks": "Weeks 8-10",
                    "focus_course_id": c3.get("course_id", "C003"),
                    "focus_course_title": c3.get("title", "Advanced Engineering"),
                    "core_skills": c3.get("skills_covered", ["Optimization", "Scalability"])[:3],
                    "milestone_deliverable": f"Implement comprehensive test suites and benchmarking for {role} role."
                },
                {
                    "phase_number": 4,
                    "title": "Capstone Engineering & Professional Portfolio",
                    "weeks": "Weeks 11-12",
                    "focus_course_id": "CAPSTONE",
                    "focus_course_title": f"{role} Portfolio Capstone",
                    "core_skills": ["Full Pipeline Integration", "Deployment", "Documentation"],
                    "milestone_deliverable": "Publish open-source GitHub repository with demo video and live deployment."
                }
            ],
            "capstone_project": {
                "title": f"End-to-End {role} Showcase Platform",
                "description": f"Build and deploy a scalable, real-world application highlighting your new competencies in {role}.",
                "tech_stack": ["Python / JavaScript", "Docker / Cloud", "REST / Microservices"]
            },
            "certification_recommendation": f"Prepare for recognized {role} industry certification exam upon finishing Phase 3."
        }
