"""
Profiler Agent (User Profiler & Needs Assessment)
Deconstructs learner input into structured learning goals, skill gaps,
timeline constraints, and prioritized search queries.
"""

import json
import re
from typing import Dict, Any, Optional
from .base_agent import BaseAgent


class ProfilerAgent(BaseAgent):
    def __init__(self, provider: str = "offline", api_key: Optional[str] = None, model: Optional[str] = None):
        super().__init__(
            name="ProfilerAgent",
            role="Educational Counselor & Diagnostic Assessor",
            provider=provider,
            api_key=api_key,
            model=model
        )

    def analyze_profile(
        self,
        user_query: str,
        experience_level: str = "Beginner",
        target_role: str = "Software Engineer",
        hours_per_week: int = 10,
        preferred_learning_style: str = "Hands-on Project Oriented",
        budget_preference: str = "All (Free & Paid)"
    ) -> Dict[str, Any]:
        """
        Processes learner attributes and extracts structured needs profile.
        """
        system_prompt = (
            "You are an expert Pedagogical Profiler and Career Counselor Agent.\n"
            "Analyze the student's background, desired role, and learning preferences.\n"
            "Respond ONLY in valid JSON format with keys:\n"
            "- target_role: string\n"
            "- current_level: string\n"
            "- target_level: string\n"
            "- skill_gaps: list of strings (4-6 high-impact technical skills needed)\n"
            "- learning_style: string\n"
            "- hours_per_week: int\n"
            "- search_keywords: list of strings (4-8 optimized search terms)\n"
            "- pedagogical_strategy: string (brief 2-sentence guidance)\n"
        )

        user_prompt = (
            f"User Goal/Query: {user_query}\n"
            f"Declared Experience: {experience_level}\n"
            f"Target Role: {target_role}\n"
            f"Weekly Time Commitment: {hours_per_week} hours/week\n"
            f"Preferred Style: {preferred_learning_style}\n"
            f"Budget Constraint: {budget_preference}\n"
        )

        llm_response = self.call_llm(system_prompt, user_prompt, temperature=0.2)
        raw_text = llm_response["content"]

        try:
            # Clean markdown codeblocks if LLM returned ```json ... ```
            cleaned = re.sub(r"^```json\s*", "", raw_text.strip(), flags=re.MULTILINE)
            cleaned = re.sub(r"^```\s*", "", cleaned.strip(), flags=re.MULTILINE)
            profile_data = json.loads(cleaned)
        except Exception:
            profile_data = self._heuristic_parse(
                user_query, experience_level, target_role, hours_per_week, preferred_learning_style
            )

        # Attach metadata
        profile_data["_meta"] = {
            "agent": self.name,
            "role": self.role,
            "duration_s": llm_response["duration_s"],
            "provider": llm_response["provider"],
            "model": llm_response["model"]
        }
        return profile_data

    def _heuristic_fallback(
        self,
        system_prompt: str,
        user_prompt: str,
        fallback_reason: Optional[str] = None
    ) -> str:
        # Generate clean JSON heuristic
        # Extract target role and level from user_prompt
        role_match = re.search(r"Target Role:\s*(.+)", user_prompt)
        role = role_match.group(1).strip() if role_match else "Software Engineer"
        level_match = re.search(r"Declared Experience:\s*(.+)", user_prompt)
        level = level_match.group(1).strip() if level_match else "Beginner"

        skills = self._derive_skills_for_role(role)
        search_terms = [role] + skills[:4]

        data = {
            "target_role": role,
            "current_level": level,
            "target_level": "Intermediate" if level.lower() == "beginner" else "Advanced",
            "skill_gaps": skills,
            "learning_style": "Hands-on Project Oriented",
            "hours_per_week": 10,
            "search_keywords": search_terms,
            "pedagogical_strategy": f"Focus on building solid foundational theory in {skills[0]} before transitioning to applied projects in {skills[1]}."
        }
        return json.dumps(data, indent=2)

    def _heuristic_parse(
        self,
        query: str,
        level: str,
        role: str,
        hours: int,
        style: str
    ) -> Dict[str, Any]:
        skills = self._derive_skills_for_role(role or query)
        search_terms = [role, query] + skills[:3]
        return {
            "target_role": role,
            "current_level": level,
            "target_level": "Intermediate" if level.lower() == "beginner" else "Advanced",
            "skill_gaps": skills,
            "learning_style": style,
            "hours_per_week": hours,
            "search_keywords": [s for s in search_terms if s],
            "pedagogical_strategy": f"Prioritize core syntax and fundamentals of {skills[0]} followed by hands-on capstone portfolio work."
        }

    def _derive_skills_for_role(self, role: str) -> list:
        role_lower = role.lower()
        if "ai" in role_lower or "machine learning" in role_lower or "data science" in role_lower:
            return ["Python", "Linear Algebra", "Supervised Learning", "Deep Learning", "PyTorch", "Model Evaluation"]
        elif "web" in role_lower or "frontend" in role_lower or "full stack" in role_lower:
            return ["JavaScript/TypeScript", "React", "Node.js", "REST APIs", "State Management", "Database Design"]
        elif "cloud" in role_lower or "devops" in role_lower:
            return ["Linux CLI", "Docker", "Kubernetes", "AWS/GCP Cloud Architecture", "CI/CD Pipelines", "Terraform"]
        elif "cyber" in role_lower or "security" in role_lower:
            return ["Network Security", "Cryptography", "Penetration Testing", "Threat Analysis", "Linux/Bash", "SIEM Tools"]
        elif "mobile" in role_lower or "app" in role_lower:
            return ["Flutter/Dart", "Swift/iOS", "Kotlin/Android", "Mobile Architecture", "REST Integration", "Local Storage"]
        elif "design" in role_lower or "ux" in role_lower or "ui" in role_lower:
            return ["User Research", "Figma Prototyping", "Wireframing", "Design Systems", "Usability Testing", "Information Architecture"]
        else:
            return ["Data Structures", "Algorithms", "Object-Oriented Programming", "System Design", "Git Version Control", "Testing"]
