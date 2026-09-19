"""
EduAgent: Multi-Agent Course Recommendation & Learning Path Orchestrator
Interactive Gradio Web Application with Multi-Provider LLM & Offline Heuristic Engine
"""

import os
import json
import time
from typing import Dict, Any, List, Tuple
import pandas as pd
import gradio as gr

from engine.recommender import CourseRecommenderEngine
from orchestrator.orchestrator import MultiAgentOrchestrator

# Initialize core services
engine = CourseRecommenderEngine()
orchestrator = MultiAgentOrchestrator(engine=engine, provider="offline")

# Custom CSS for modern visual design
CUSTOM_CSS = """
/* Modern Dark Glassmorphism Theme */
:root {
    --primary-gradient: linear-gradient(135deg, #6366f1 0%, #4338ca 100%);
    --card-bg: #1e1e2f;
    --card-border: #2e2e48;
    --accent-color: #38bdf8;
    --accent-emerald: #10b981;
    --accent-amber: #f59e0b;
}

body, .gradio-container {
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif !important;
}

.main-header {
    background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
    border: 1px solid #3730a3;
    border-radius: 16px;
    padding: 24px 32px;
    margin-bottom: 24px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
}

.main-header h1 {
    color: #ffffff;
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.main-header p {
    color: #94a3b8;
    font-size: 1.05rem;
    margin: 0;
}

.agent-badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    background: rgba(99, 102, 241, 0.2);
    color: #a5b4fc;
    border: 1px solid #6366f1;
    margin-right: 6px;
}

.course-card {
    background: #181826;
    border: 1px solid #2d2d44;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 18px;
    transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
}

.course-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.35);
    border-color: #6366f1;
}

.course-card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 10px;
}

.course-title {
    color: #f8fafc;
    font-size: 1.2rem;
    font-weight: 600;
    margin: 0 0 6px 0;
}

.course-provider {
    color: #94a3b8;
    font-size: 0.85rem;
}

.match-pill {
    background: #064e3b;
    color: #34d399;
    border: 1px solid #059669;
    padding: 4px 12px;
    border-radius: 9999px;
    font-weight: 700;
    font-size: 0.85rem;
}

.tag-pill {
    background: #1f2937;
    color: #93c5fd;
    border: 1px solid #374151;
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 0.75rem;
    display: inline-block;
    margin: 2px 4px 2px 0;
}

.why-recommended-box {
    background: #111827;
    border-left: 3px solid #38bdf8;
    padding: 10px 14px;
    border-radius: 0 8px 8px 0;
    margin: 12px 0;
    color: #cbd5e1;
    font-size: 0.9rem;
}

.enroll-btn {
    display: inline-block;
    background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%);
    color: #ffffff !important;
    text-decoration: none !important;
    padding: 6px 16px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.85rem;
    margin-top: 8px;
    transition: opacity 0.2s;
}

.enroll-btn:hover {
    opacity: 0.9;
}

.phase-card {
    background: #181826;
    border-left: 4px solid #6366f1;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 14px;
}

.stat-box {
    background: #181826;
    border: 1px solid #2e2e48;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
}

.stat-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #38bdf8;
}

.stat-label {
    font-size: 0.85rem;
    color: #94a3b8;
    margin-top: 4px;
}
"""


def build_course_cards_html(courses: List[Dict[str, Any]]) -> str:
    if not courses:
        return "<p style='color:#94a3b8; padding:20px; text-align:center;'>No courses matching your criteria. Try adjusting your query or constraints.</p>"

    html_parts = []
    for c in courses:
        price_str = "FREE" if c.get("is_free") else f"${c.get('price_usd', 0):.2f}"
        price_color = "#34d399" if c.get("is_free") else "#fbbf24"
        skills = c.get("skills_covered", [])
        skills_html = "".join([f"<span class='tag-pill'>{s}</span>" for s in skills[:5]])

        html_parts.append(f"""
        <div class="course-card">
            <div class="course-card-header">
                <div>
                    <h3 class="course-title">{c.get('title')}</h3>
                    <div class="course-provider">🏛️ {c.get('provider')} &nbsp;•&nbsp; 🏷️ {c.get('category')} &nbsp;•&nbsp; ⚡ Level: <strong>{c.get('level')}</strong></div>
                </div>
                <div class="match-pill">{c.get('match_percentage', 90)}% Match</div>
            </div>
            
            <p style="color: #94a3b8; font-size: 0.9rem; margin: 8px 0;">{c.get('description')}</p>
            
            <div class="why-recommended-box">
                <strong>🤖 Agent Insight:</strong> {c.get('why_recommended', 'Highly aligned with your career goals and current skill profile.')}
            </div>
            
            <div style="margin: 10px 0;">
                <span style="color:#94a3b8; font-size:0.8rem; margin-right:6px;">Skills:</span> {skills_html}
            </div>
            
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:14px; padding-top:10px; border-top:1px solid #232338;">
                <div style="font-size:0.85rem; color:#cbd5e1;">
                    ⭐ <strong>{c.get('rating')}</strong> &nbsp;|&nbsp; ⏱️ <strong>{c.get('duration_hours')} hrs</strong> &nbsp;|&nbsp; 💵 <span style="color:{price_color}; font-weight:700;">{price_str}</span>
                </div>
                <a href="{c.get('url')}" target="_blank" class="enroll-btn">Explore Course ↗</a>
            </div>
        </div>
        """)
    return "".join(html_parts)


def build_roadmap_html(roadmap: Dict[str, Any], critique: Dict[str, Any]) -> str:
    phases = roadmap.get("phases", [])
    capstone = roadmap.get("capstone_project", {})

    feasibility = critique.get("feasibility_score", 90)
    feas_color = "#34d399" if feasibility >= 80 else "#fbbf24"

    header_html = f"""
    <div style="display:flex; gap:16px; margin-bottom:20px;">
        <div class="stat-box" style="flex:1;">
            <div class="stat-value">{roadmap.get('total_estimated_weeks', 12)} Weeks</div>
            <div class="stat-label">Total Estimated Duration</div>
        </div>
        <div class="stat-box" style="flex:1;">
            <div class="stat-value" style="color:{feas_color};">{feasibility}%</div>
            <div class="stat-label">Critic Feasibility Score</div>
        </div>
        <div class="stat-box" style="flex:1;">
            <div class="stat-value">{critique.get('total_course_hours', 120)} hrs</div>
            <div class="stat-label">Total Curriculum Study</div>
        </div>
    </div>
    """

    phases_html = []
    for p in phases:
        skills = p.get("core_skills", [])
        skills_pills = " ".join([f"<span class='tag-pill'>{s}</span>" for s in skills])
        phases_html.append(f"""
        <div class="phase-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <h4 style="margin:0; color:#e2e8f0; font-size:1.1rem;">Phase {p.get('phase_number')}: {p.get('title')}</h4>
                <span class="match-pill" style="background:#1e1b4b; color:#a5b4fc; border-color:#4338ca;">{p.get('weeks')}</span>
            </div>
            <p style="color:#94a3b8; font-size:0.9rem; margin:6px 0;"><strong>Anchor Course:</strong> {p.get('focus_course_title')} ({p.get('focus_course_id')})</p>
            <div style="margin:8px 0;">{skills_pills}</div>
            <div style="background:#111827; padding:8px 12px; border-radius:6px; font-size:0.85rem; color:#cbd5e1; margin-top:8px;">
                🎯 <strong>Milestone Deliverable:</strong> {p.get('milestone_deliverable')}
            </div>
        </div>
        """)

    capstone_html = f"""
    <div style="background: linear-gradient(135deg, #1e1b4b 0%, #172554 100%); border: 1px solid #3b82f6; border-radius:12px; padding:20px; margin-top:20px;">
        <h4 style="color:#ffffff; margin:0 0 8px 0; font-size:1.15rem;">🚀 Capstone Portfolio Project: {capstone.get('title', 'Domain Project')}</h4>
        <p style="color:#cbd5e1; font-size:0.9rem; margin-bottom:12px;">{capstone.get('description', 'Comprehensive end-to-end implementation project.')}</p>
        <p style="color:#94a3b8; font-size:0.85rem; margin:0;"><strong>Recommended Tech Stack:</strong> {', '.join(capstone.get('tech_stack', []))}</p>
        <div style="margin-top:12px; font-size:0.85rem; color:#a5b4fc;">
            🎓 <strong>Industry Credential Target:</strong> {roadmap.get('certification_recommendation', 'Target relevant domain certificate.')}
        </div>
    </div>
    """

    critique_box = f"""
    <div style="background:#181826; border:1px solid #374151; border-radius:12px; padding:18px; margin-top:20px;">
        <h4 style="color:#f8fafc; margin:0 0 10px 0; font-size:1.05rem;">📋 Pedagogical Auditor Verdict</h4>
        <p style="color:#cbd5e1; font-size:0.9rem; margin-bottom:10px;">{critique.get('verdict_summary')}</p>
        <p style="color:#94a3b8; font-size:0.85rem; margin-bottom:4px;"><strong>Prerequisite Evaluation:</strong> {critique.get('prerequisite_audit')}</p>
        <div style="margin-top:8px;">
            <strong style="color:#fbbf24; font-size:0.85rem;">⚠️ Potential Bottlenecks:</strong>
            <ul style="color:#cbd5e1; font-size:0.85rem; margin:4px 0 8px 20px;">
                {''.join([f'<li>{b}</li>' for b in critique.get('potential_bottlenecks', [])])}
            </ul>
            <strong style="color:#34d399; font-size:0.85rem;">💡 Actionable Study Tips:</strong>
            <ul style="color:#cbd5e1; font-size:0.85rem; margin:4px 0 0 20px;">
                {''.join([f'<li>{tip}</li>' for tip in critique.get('actionable_recommendations', [])])}
            </ul>
        </div>
    </div>
    """

    return header_html + "".join(phases_html) + capstone_html + critique_box


def run_recommendation(
    user_query: str,
    experience_level: str,
    target_role: str,
    hours_per_week: int,
    learning_style: str,
    budget_preference: str,
    category_filter: str,
    top_k: int
) -> Tuple[str, str, pd.DataFrame, str]:
    if not user_query.strip():
        user_query = f"I want to become a {target_role} starting from {experience_level} level."

    cat_arg = None if category_filter == "All" else category_filter

    res = orchestrator.run_pipeline(
        user_query=user_query,
        experience_level=experience_level,
        target_role=target_role,
        hours_per_week=int(hours_per_week),
        preferred_learning_style=learning_style,
        budget_preference=budget_preference,
        preferred_category=cat_arg,
        top_k=int(top_k)
    )

    profile = res["profile"]
    courses = res["courses"]
    roadmap = res["roadmap"]
    critique = res["critique"]
    trace = res["trace"]

    # Diagnostic header
    gaps = ", ".join(profile.get("skill_gaps", [])[:4])
    diag_html = f"""
    <div style="background:#181826; border:1px solid #3b82f6; border-radius:10px; padding:14px 18px; margin-bottom:16px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span class="agent-badge">Profiler Agent Diagnosed</span>
                <strong style="color:#f8fafc; font-size:1.05rem;">{profile.get('target_role')}</strong>
                <span style="color:#94a3b8; font-size:0.85rem;">(Current: {profile.get('current_level')} → Target: {profile.get('target_level')})</span>
            </div>
            <div style="color:#38bdf8; font-size:0.85rem; font-weight:600;">⏱️ {res['metrics']['total_pipeline_latency_s']}s Orchestration</div>
        </div>
        <div style="margin-top:8px; font-size:0.85rem; color:#cbd5e1;">
            🎯 <strong>Prioritized Skill Gaps:</strong> {gaps}
        </div>
        <div style="margin-top:4px; font-size:0.85rem; color:#94a3b8;">
            🧭 <strong>Pedagogical Strategy:</strong> {profile.get('pedagogical_strategy')}
        </div>
    </div>
    """

    courses_html = build_course_cards_html(courses)
    roadmap_html = build_roadmap_html(roadmap, critique)

    # Trace DataFrame
    trace_df = pd.DataFrame(trace)[["timestamp", "agent", "action", "duration_seconds", "details"]]
    trace_df.columns = ["Timestamp (s)", "Agent", "Action", "Latency (s)", "Details"]

    # Full JSON export
    full_json = json.dumps(res, indent=2)

    return diag_html + courses_html, roadmap_html, trace_df, full_json


def apply_preset(preset_name: str):
    presets = {
        "Aspiring AI Engineer": (
            "I want to master modern Machine Learning, Deep Learning, and PyTorch to build neural networks and AI models.",
            "Beginner",
            "AI & Machine Learning Engineer",
            12,
            "Hands-on Project Oriented",
            "All (Free & Paid)",
            "AI & Machine Learning"
        ),
        "Full Stack Web Dev": (
            "Looking to build modern responsive full stack applications with React, Next.js, Node.js, and databases.",
            "Beginner",
            "Full Stack Web Developer",
            15,
            "Hands-on Project Oriented",
            "All (Free & Paid)",
            "Web Development"
        ),
        "Cloud & DevOps Architect": (
            "Want to master Docker, Kubernetes, AWS cloud architectures, and automated CI/CD deployment pipelines.",
            "Intermediate",
            "Cloud & DevOps Engineer",
            10,
            "Certification Focused",
            "All (Free & Paid)",
            "Cloud & DevOps"
        ),
        "Ethical Hacker & Security Analyst": (
            "Want to learn cybersecurity fundamentals, penetration testing, network defense, and CompTIA Security+ concepts.",
            "Beginner",
            "Cybersecurity Analyst",
            10,
            "Hands-on Project Oriented",
            "Free Only",
            "Cybersecurity"
        )
    }
    return presets.get(preset_name, presets["Aspiring AI Engineer"])


def update_orchestrator_settings(provider: str, api_key: str, model: str):
    prov_key = "offline"
    if "Groq" in provider:
        prov_key = "groq"
    elif "Gemini" in provider:
        prov_key = "gemini"
    elif "OpenAI" in provider:
        prov_key = "openai"

    orchestrator.update_configuration(
        provider=prov_key,
        api_key=api_key.strip() if api_key else None,
        model=model.strip() if model else None
    )
    status_msg = f"✅ Orchestrator updated to **{provider}** (Model: `{orchestrator.model}`)."
    if prov_key == "offline":
        status_msg += " Using ultra-fast built-in deterministic heuristic engine. No API key needed!"
    return status_msg


# Build Gradio UI
with gr.Blocks(title="EduAgent - Multi-Agent Course Recommendation System") as demo:
    gr.HTML("""
    <div class="main-header">
        <h1>🎓 EduAgent: AI Course Recommendation & Learning Path Orchestrator</h1>
        <p>A Multi-Agent System coordinating Pedagogical Profiling, Hybrid Vector Search, Curriculum Roadmap Synthesis, and Quality Auditing.</p>
    </div>
    """)

    with gr.Tabs() as tabs:
        # -------------------------------------------------------------
        # TAB 1: Course Recommender & Planner
        # -------------------------------------------------------------
        with gr.Tab("🎯 AI Course Recommender", id="tab_recommender"):
            with gr.Row():
                # Left column: input controls
                with gr.Column(scale=4):
                    gr.Markdown("### 👤 Learner Profile & Goals")
                    
                    with gr.Row():
                        preset_ai = gr.Button("🤖 Aspiring AI", size="sm")
                        preset_web = gr.Button("💻 Full Stack", size="sm")
                        preset_cloud = gr.Button("☁️ Cloud/DevOps", size="sm")
                        preset_sec = gr.Button("🔒 CyberSec", size="sm")

                    user_query_input = gr.Textbox(
                        label="Describe Your Background & Career Aspirations",
                        placeholder="e.g. I know basic Python and want to transition into Machine Learning and deep learning in 3 months...",
                        lines=3,
                        value="I know Python basics and want to become an AI Engineer capable of training neural networks."
                    )

                    with gr.Row():
                        target_role_input = gr.Dropdown(
                            choices=[
                                "AI & Machine Learning Engineer",
                                "Full Stack Web Developer",
                                "Data Scientist",
                                "Cloud & DevOps Engineer",
                                "Cybersecurity Analyst",
                                "Mobile App Developer",
                                "UI/UX & Product Designer",
                                "Software Engineer"
                            ],
                            value="AI & Machine Learning Engineer",
                            label="Target Role"
                        )
                        experience_level_input = gr.Dropdown(
                            choices=["Beginner", "Intermediate", "Advanced"],
                            value="Beginner",
                            label="Current Experience Level"
                        )

                    with gr.Row():
                        hours_input = gr.Slider(
                            minimum=4,
                            maximum=40,
                            value=12,
                            step=2,
                            label="Weekly Time Commitment (Hours/Week)"
                        )
                        top_k_input = gr.Slider(
                            minimum=2,
                            maximum=8,
                            value=4,
                            step=1,
                            label="Recommendations Count"
                        )

                    with gr.Row():
                        learning_style_input = gr.Dropdown(
                            choices=[
                                "Hands-on Project Oriented",
                                "Theory & Mathematical Rigor",
                                "Fast-track Interview Prep",
                                "Certification Focused"
                            ],
                            value="Hands-on Project Oriented",
                            label="Learning Preference"
                        )
                        budget_input = gr.Dropdown(
                            choices=["All (Free & Paid)", "Free Only"],
                            value="All (Free & Paid)",
                            label="Budget Constraint"
                        )

                    category_input = gr.Dropdown(
                        choices=engine.get_categories(),
                        value="All",
                        label="Primary Domain Category Filter"
                    )

                    recommend_btn = gr.Button("🚀 Orchestrate Course Recommendations", variant="primary", size="lg")

                # Right column: Output Cards
                with gr.Column(scale=6):
                    gr.Markdown("### 📚 Recommended Courses & Pedagogical Diagnostics")
                    courses_output = gr.HTML("<p style='color:#94a3b8; padding:30px; text-align:center;'>Click 'Orchestrate Course Recommendations' to trigger the multi-agent pipeline.</p>")

        # -------------------------------------------------------------
        # TAB 2: Learning Roadmap & Timeline
        # -------------------------------------------------------------
        with gr.Tab("🗺️ Career Learning Roadmap", id="tab_roadmap"):
            gr.Markdown("### 📅 Sequenced 4-Phase Learning Path & Milestone Schedule")
            roadmap_output = gr.HTML("<p style='color:#94a3b8; padding:30px; text-align:center;'>Run recommendations first in Tab 1 to generate your tailored curriculum roadmap.</p>")

        # -------------------------------------------------------------
        # TAB 3: Course Explorer & Dataset
        # -------------------------------------------------------------
        with gr.Tab("📊 Course Catalog Explorer", id="tab_catalog"):
            gr.Markdown("### 🔍 Interactive Course Database (100 Curated Courses)")
            with gr.Row():
                catalog_search = gr.Textbox(label="Filter by Keyword / Skill / Title", placeholder="e.g. Python, Docker, React, AWS...")
                catalog_cat = gr.Dropdown(choices=engine.get_categories(), value="All", label="Category")
                catalog_lvl = gr.Dropdown(choices=["All", "Beginner", "Intermediate", "Advanced"], value="All", label="Level")

            catalog_df_view = gr.DataFrame(
                value=engine.df[["course_id", "title", "provider", "category", "level", "rating", "duration_hours", "price_usd", "skills_covered"]],
                interactive=False,
                wrap=True
            )

            def filter_catalog(query, cat, lvl):
                df = engine.df.copy()
                if query and query.strip():
                    q = query.lower()
                    mask = (
                        df["title"].str.lower().str.contains(q) |
                        df["skills_covered"].str.lower().str.contains(q) |
                        df["provider"].str.lower().str.contains(q)
                    )
                    df = df[mask]
                if cat != "All":
                    df = df[df["category"] == cat]
                if lvl != "All":
                    df = df[df["level"] == lvl]
                return df[["course_id", "title", "provider", "category", "level", "rating", "duration_hours", "price_usd", "skills_covered"]]

            catalog_search.change(filter_catalog, inputs=[catalog_search, catalog_cat, catalog_lvl], outputs=[catalog_df_view])
            catalog_cat.change(filter_catalog, inputs=[catalog_search, catalog_cat, catalog_lvl], outputs=[catalog_df_view])
            catalog_lvl.change(filter_catalog, inputs=[catalog_search, catalog_cat, catalog_lvl], outputs=[catalog_df_view])

        # -------------------------------------------------------------
        # TAB 4: Multi-Agent Architecture & Trace Visualizer
        # -------------------------------------------------------------
        with gr.Tab("🤖 Agent Architecture & Trace", id="tab_trace"):
            gr.Markdown("### 🔬 Multi-Agent Execution Flow & Diagnostics")
            
            gr.Markdown("""
            ```
            [Student Query & Preferences]
                         │
                         ▼
             [ 1. ProfilerAgent ]  ───► Extracts goals, skill gaps, & optimal queries
                         │
                         ▼
             [ 2. RetrievalAgent ] ───► Hybrid TF-IDF + Cosine Similarity + Metadata Ranking
                         │
                         ▼
             [ 3. PathPlannerAgent ] ─► Assembles 4-Phase Chronological Roadmap & Capstone
                         │
                         ▼
             [ 4. CriticAgent ]    ───► Audits workload feasibility, prerequisites, & study risks
                         │
                         ▼
            [ Consolidated UI & Explainable Recommendations ]
            ```
            """)
            
            gr.Markdown("#### ⏱️ Real-time Pipeline Execution Trace")
            trace_table = gr.DataFrame(
                headers=["Timestamp (s)", "Agent", "Action", "Latency (s)", "Details"],
                interactive=False
            )
            
            gr.Markdown("#### 📦 Complete State JSON Payload")
            json_inspector = gr.Code(label="Orchestrator State JSON", language="json")

        # -------------------------------------------------------------
        # TAB 5: Settings & Model Configuration
        # -------------------------------------------------------------
        with gr.Tab("⚙️ Settings & API Config", id="tab_settings"):
            gr.Markdown("### 🔧 LLM Provider & Execution Engine Settings")
            gr.Markdown(
                "You can run EduAgent with **zero setup** using the built-in **Local Heuristic Engine**, "
                "or connect your API key for **Groq, OpenAI, or Google Gemini**."
            )

            with gr.Row():
                with gr.Column():
                    provider_dropdown = gr.Dropdown(
                        choices=[
                            "Offline Heuristic Engine (No API Key Required)",
                            "Groq (Llama-3.3-70B - Free & Ultra Fast)",
                            "Google Gemini (Gemini-1.5-Flash)",
                            "OpenAI (GPT-4o-mini)"
                        ],
                        value="Offline Heuristic Engine (No API Key Required)",
                        label="Active LLM Backend"
                    )
                    api_key_box = gr.Textbox(
                        label="API Key (Leave blank for Offline Mode)",
                        type="password",
                        placeholder="e.g. gsk_... or AIza... or sk-..."
                    )
                    model_box = gr.Textbox(
                        label="Model Identifier Override (Optional)",
                        placeholder="Leave blank to use provider default"
                    )
                    save_settings_btn = gr.Button("💾 Save & Apply Backend Settings", variant="primary")
                    settings_status = gr.Markdown("Current Status: **Offline Heuristic Mode (Ready for Viva Demo)**")

                    save_settings_btn.click(
                        update_orchestrator_settings,
                        inputs=[provider_dropdown, api_key_box, model_box],
                        outputs=[settings_status]
            )

    # Preset triggers
    preset_ai.click(lambda: apply_preset("Aspiring AI Engineer"), outputs=[user_query_input, experience_level_input, target_role_input, hours_input, learning_style_input, budget_input, category_input])
    preset_web.click(lambda: apply_preset("Full Stack Web Dev"), outputs=[user_query_input, experience_level_input, target_role_input, hours_input, learning_style_input, budget_input, category_input])
    preset_cloud.click(lambda: apply_preset("Cloud & DevOps Architect"), outputs=[user_query_input, experience_level_input, target_role_input, hours_input, learning_style_input, budget_input, category_input])
    preset_sec.click(lambda: apply_preset("Ethical Hacker & Security Analyst"), outputs=[user_query_input, experience_level_input, target_role_input, hours_input, learning_style_input, budget_input, category_input])

    # Main recommendation pipeline trigger
    recommend_btn.click(
        run_recommendation,
        inputs=[
            user_query_input,
            experience_level_input,
            target_role_input,
            hours_input,
            learning_style_input,
            budget_input,
            category_input,
            top_k_input
        ],
        outputs=[courses_output, roadmap_output, trace_table, json_inspector]
    )

if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        theme=gr.themes.Soft(primary_hue="indigo"),
        css=CUSTOM_CSS
    )
