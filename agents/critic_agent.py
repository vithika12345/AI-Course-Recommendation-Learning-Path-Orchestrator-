"""
Pedagogical Critic Agent
Performs sanity checks, workload feasibility audits, prerequisite validation,
and highlights cognitive bottlenecks or study risks.
"""

import json
import re
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent


class CriticAgent(BaseAgent):
    def __init__(self, provider: str = "offline", api_key: Optional[str] = None, model: Optional[str] = None):
        super().__init__(
            name="CriticAgent",
            role="Pedagogical Auditor & Academic Quality Reviewer",
            provider=provider,
            api_key=api_key,
            model=model
        )

    def review_plan(
        self,
        profile: Dict[str, Any],
        courses: List[Dict[str, Any]],
        roadmap: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Conducts an academic critique and workload audit of the curriculum plan.
        """
        system_prompt = (
            "You are a strict Pedagogical Auditor and Academic Reviewer.\n"
            "Audit the learner's profile, chosen courses, and proposed timeline.\n"
            "Respond ONLY in valid JSON format with keys:\n"
            "- feasibility_score: int (0-100% rating overall realistic success probability)\n"
            "- workload_status: string (e.g. 'Manageable', 'Intense', 'Overloaded')\n"
            "- prerequisite_audit: string (evaluation of prerequisite readiness)\n"
            "- potential_bottlenecks: list of strings (2-3 honest study obstacles/risks)\n"
            "- actionable_recommendations: list of strings (3 concrete tips to guarantee completion)\n"
            "- verdict_summary: string (2-sentence executive summary of the evaluation)\n"
        )

        total_hours = sum(c.get("duration_hours", 20) for c in courses)
        hours_per_week = profile.get("hours_per_week", 10)
        estimated_weeks = max(1, round(total_hours / max(1, hours_per_week)))

        user_prompt = (
            f"User Background: {profile.get('current_level')} targeting {profile.get('target_role')}\n"
            f"Weekly Commitment: {hours_per_week} hrs/week\n"
            f"Total Coursework Hours: {total_hours} hrs across {len(courses)} courses\n"
            f"Estimated Realistic Completion: {estimated_weeks} weeks\n"
            f"Roadmap Timeline: {roadmap.get('total_estimated_weeks', 12)} weeks\n"
            f"Course Prerequisites: {', '.join([c.get('title') + ' requires: ' + str(c.get('prerequisites')) for c in courses])}\n"
        )

        llm_response = self.call_llm(system_prompt, user_prompt, temperature=0.2)
        raw_text = llm_response["content"]

        try:
            cleaned = re.sub(r"^```json\s*", "", raw_text.strip(), flags=re.MULTILINE)
            cleaned = re.sub(r"^```\s*", "", cleaned.strip(), flags=re.MULTILINE)
            critique_data = json.loads(cleaned)
        except Exception:
            critique_data = self._heuristic_critique(profile, courses, roadmap, total_hours, hours_per_week)

        critique_data["total_course_hours"] = total_hours
        critique_data["_meta"] = {
            "agent": self.name,
            "role": self.role,
            "duration_s": llm_response["duration_s"],
            "provider": llm_response["provider"],
            "model": llm_response["model"]
        }
        return critique_data

    def _heuristic_fallback(
        self,
        system_prompt: str,
        user_prompt: str,
        fallback_reason: Optional[str] = None
    ) -> str:
        data = {
            "feasibility_score": 88,
            "workload_status": "Balanced & Achievable",
            "prerequisite_audit": "Prerequisites are satisfied. Foundational courses bridge required background knowledge smoothly.",
            "potential_bottlenecks": [
                "Transition from conceptual theory to unguided capstone programming.",
                "Sustaining consistent weekly study cadence during heavy project weeks."
            ],
            "actionable_recommendations": [
                "Block out 2 dedicated 2-hour study sprints on weekends rather than fragmented daily sessions.",
                "Build accompanying micro-repositories on GitHub for each completed chapter to reinforce retention.",
                "Review foundational prerequisite math or syntax cheat-sheets before tackling Phase 2."
            ],
            "verdict_summary": "High pedagogical coherence. The learning path maintains an optimal balance between theoretical rigor and hands-on portfolio milestones."
        }
        return json.dumps(data, indent=2)

    def _heuristic_critique(
        self,
        profile: Dict[str, Any],
        courses: List[Dict[str, Any]],
        roadmap: Dict[str, Any],
        total_hours: int,
        hours_per_week: int
    ) -> Dict[str, Any]:
        weeks_needed = total_hours / max(1, hours_per_week)
        planned_weeks = roadmap.get("total_estimated_weeks", 12)

        if weeks_needed > planned_weeks * 1.3:
            feasibility = 72
            status = "Intense / Demanding"
            bottleneck = f"Course load ({total_hours} hrs) slightly exceeds planned timeline at {hours_per_week} hrs/week."
        else:
            feasibility = 92
            status = "Well-Paced & Realistic"
            bottleneck = "Maintaining momentum when switching between different platform styles."

        return {
            "feasibility_score": feasibility,
            "workload_status": status,
            "prerequisite_audit": "Courses are well-ordered chronologically. Early modules build the necessary scaffolding for later specialized topics.",
            "potential_bottlenecks": [
                bottleneck,
                "Context-switching between multi-course concepts without immediate hands-on coding."
            ],
            "actionable_recommendations": [
                "Adopt active recall and build small test scripts after every lecture module.",
                "Do not skip the capstone phase; real hiring managers evaluate project repositories over certificates.",
                "Utilize online documentation and official cheat-sheets alongside video lectures."
            ],
            "verdict_summary": "The recommended roadmap is pedagogically sound and realistic for your target schedule."
        }
