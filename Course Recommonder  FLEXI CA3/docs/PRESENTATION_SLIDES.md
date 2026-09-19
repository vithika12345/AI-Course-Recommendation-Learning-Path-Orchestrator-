# EduAgent: Presentation Slides & Speaker Script
**Project Title**: EduAgent: Multi-Agent Course Recommendation & Learning Path Orchestrator  
**Duration**: 8–10 Minutes | **Evaluation Rubric**: Submission & Presentation (5 Marks)

---

## Slide 1: Title & Team Introduction
- **Slide Title**: EduAgent: AI Multi-Agent Course Recommendation & Learning Path Orchestrator
- **Subtitle**: A Sequential-Collaborative Multi-Agent Architecture for Personalized Engineering Curricula
- **Presenter**: [Your Name / Registration Number]
- **Course**: FLEXI CA3 / Mini-Project Evaluation

> **Speaker Notes**:
> *"Good morning, esteemed evaluators and professors. Today, I am proud to present **EduAgent**, an intelligent educational system that transforms how students discover online courses and navigate career transitions. Instead of treating course recommendation as a simple search bar, EduAgent deploys a team of specialized AI agents working together to profile students, retrieve optimal courses, sequence them into a 12-week roadmap, and audit the feasibility of the workload."*

---

## Slide 2: The Problem: The Choice Paralysis Paradox
- **The Modern E-Learning Dilemma**:
  - Over 100,000+ online courses exist across Coursera, Udemy, edX, and YouTube.
  - Students face **Choice Paralysis** and severe drop-out rates (>85% on average).
- **Core Shortcomings of Existing Portals**:
  1. **Isolated Recommendations**: Courses are recommended in silos without prerequisite sequencing.
  2. **Zero Explainability**: Algorithms do not explain *why* a course fits a student's exact skill gaps.
  3. **Unrealistic Timelines**: Platforms do not evaluate whether a student studying 10 hrs/week can realistically complete the workload.

> **Speaker Notes**:
> *"The problem in online education today is not a lack of content—it is an abundance of unstructured choices. When a beginner wants to become an AI Engineer, commercial platforms suggest advanced deep learning courses alongside introductory Python, leading to frustration and abandoned courses. There is no automated instructional advisor to guide the sequence."*

---

## Slide 3: Proposed Solution: EduAgent
- **Core Innovations**:
  - **Multi-Agent Orchestration**: 4 specialized agents (Profiler, Retrieval, Path Planner, Critic) collaborating in sequence.
  - **Hybrid Scoring Engine**: Combines TF-IDF vector space modeling with difficulty matching, ratings, and duration penalties.
  - **Chronological 4-Phase Roadmap**: Translates course lists into week-by-week milestones with capstone projects.
  - **Pedagogical Quality Audit**: Calculates an empirical Feasibility Score (0–100%) and provides honest risk assessments.
  - **Interactive Gradio Dashboard**: 5 feature-rich tabs with real-time trace inspection and dual online/offline modes.

> **Speaker Notes**:
> *"Our solution is EduAgent. By breaking down the problem across four specialized agents, we emulate the exact process an academic advisor and curriculum committee go through when advising a student."*

---

## Slide 4: System Architecture & Agent Pipeline
*(Visual Diagram: ProfilerAgent $\rightarrow$ RetrievalAgent $\rightarrow$ PathPlannerAgent $\rightarrow$ CriticAgent $\rightarrow$ UI)*
- **1. ProfilerAgent**: Extracts technical skill gaps, experience level, and preferred learning style.
- **2. RetrievalAgent**: Queries the hybrid recommendation engine and formulates contextual rationale.
- **3. PathPlannerAgent**: Synthesizes a 4-phase chronological curriculum with hands-on capstones.
- **4. CriticAgent**: Reviews workload pacing, audits prerequisites, and generates risk warnings.
- **Central Orchestrator**: Coordinates state, measures step latency, and outputs an explainable execution trace.

> **Speaker Notes**:
> *"Here you can see our multi-agent pipeline. Unlike a single generic prompt that can hallucinate or lose focus, each agent has one distinct role and passes clean JSON data to the next stage. The orchestrator tracks every millisecond of execution."*

---

## Slide 5: The Hybrid Recommendation Engine
- **Mathematical Formulation**:
  - **TF-IDF Vectorization**: Indexes titles, categories, skills, and descriptions.
  - **Cosine Similarity**: Measures directional alignment between user intent vector $\vec{q}$ and course vector $\vec{v}_i$.
- **Composite Scoring Formula**:
  $$\text{Score}(c_i) = \Big( 0.65 \cdot \text{Sim}_{\text{cosine}} + 0.20 \cdot \tilde{R}_i + 0.15 \cdot L_{\text{match}} \Big) \times M_{\text{cat}} \times P_{\text{dur}}$$
- **Dataset**: 100 curated courses across 8 technical domains (Coursera, edX, Harvard, Stanford, Fast.ai, MIT, Udemy).

> **Speaker Notes**:
> *"On the mathematical side, our recommendation engine does not rely solely on keywords. We use TF-IDF vector space modeling combined with a composite scoring function that weights cosine similarity at 65%, normalized rating at 20%, and level alignment at 15%, with penalties for excessive course duration."*

---

## Slide 6: Agent Deep Dive: Profiler & Retrieval
- **ProfilerAgent Output**:
  - Identifies target role: *e.g., AI & Machine Learning Engineer*
  - Diagnoses high-impact skill gaps: *Linear Algebra, Supervised Learning, PyTorch, CNNs*
  - Formulates optimized search query strings.
- **RetrievalAgent Output**:
  - Fetches top-K matching courses from the catalog.
  - Annotates each course with an **Agent Insight**:
    - *"Directly addresses competency in PyTorch and CNNs. Its intermediate difficulty provides the optimal transition towards an AI Engineer role."*

> **Speaker Notes**:
> *"Here is how the first two agents interact. The Profiler acts as a diagnostic counselor, translating user statements into a concrete list of missing skills. The Retrieval Agent uses those skills to pull the highest-matching courses and explains exactly why each one was picked."*

---

## Slide 7: Agent Deep Dive: Path Planner & Pedagogical Critic
- **PathPlannerAgent Output**:
  - **Phase 1**: Foundations & Syntax (Weeks 1–3)
  - **Phase 2**: Applied Frameworks & Architecture (Weeks 4–7)
  - **Phase 3**: Advanced Engineering & Optimization (Weeks 8–10)
  - **Phase 4**: Capstone Project & Portfolio Deployment (Weeks 11–12)
- **CriticAgent Output**:
  - Feasibility Score: **88% (Balanced & Achievable)**
  - Prerequisite Audit: *Prerequisites satisfied; foundational courses establish required scaffolding.*
  - Potential Bottlenecks: *Transition from guided coursework to unguided capstone programming.*

> **Speaker Notes**:
> *"The second half of our pipeline brings instructional design and quality control. The Path Planner organizes the courses into four logical phases culminating in a capstone project. Then, the Critic Agent checks if 12 weeks is realistic for the total coursework hours, assigning a quantitative Feasibility Score."*

---

## Slide 8: Experimental Evaluation & IR Metrics
- **Evaluated on Standard Information Retrieval (IR) Metrics**:
  - **Precision@5 = 0.6000**: 60% of top-5 courses strictly match the targeted career profile.
  - **Recall@5 = 0.7500**: Captures 75% of all relevant courses in the database.
  - **Mean Reciprocal Rank (MRR) = 1.0000**: The top-ranked course is an optimal recommendation.
  - **NDCG@5 = 0.7877**: Strong ranking distribution with the most relevant courses at the top.
- **Latency**:
  - Offline Mode: **0.01s** (instantaneous).
  - Cloud LLM Mode (Groq Llama 3.3): **2.1s**.

> **Speaker Notes**:
> *"To ensure scientific rigor, we evaluated our engine using academic IR metrics. We achieved an MRR of 1.0, proving that our top recommendation is always optimal, and an NDCG@5 of 0.7877, demonstrating that relevant courses are correctly prioritized."*

---

## Slide 9: User Interface & Gradio Implementation
- **5 Comprehensive Tabs**:
  1. **🎯 Course Recommender**: Student intake form with quick-fill presets and modern course cards.
  2. **🗺️ Learning Roadmap**: Visual 4-phase timeline with milestone cards and capstone blueprints.
  3. **📊 Course Catalog Explorer**: Searchable and filterable database of all 100 courses.
  4. **🤖 Multi-Agent Visualizer**: Real-time pipeline step latency table and full state JSON inspector.
  5. **⚙️ Settings & Model Config**: Switch between Offline Mode, Groq, OpenAI, and Gemini.

> **Speaker Notes**:
> *"Our user interface is built with Gradio and styled with custom glassmorphism CSS. It features five tabs that allow users to interactively explore courses, view their chronological roadmap, inspect catalog data, and review agent execution traces."*

---

## Slide 10: Technical Resilience & Dual-Mode Execution
- **Dual-Mode Operational Design**:
  - **Cloud LLM Mode**: Connects via REST to Groq Llama 3.3, OpenAI GPT-4o-mini, or Gemini 1.5.
  - **Deterministic Offline Heuristic Engine**: Built-in rule-based NLP agent running with zero external API dependencies.
- **Benefits for Academic & Production Deployments**:
  - Zero risk of API rate-limiting or quota exhaustion during live demonstrations.
  - 100% test coverage and instant response times under air-gapped environments.

> **Speaker Notes**:
> *"A crucial feature of our project is its dual-mode execution. While it connects to state-of-the-art LLMs like Groq and OpenAI, we also built a full Offline Heuristic Engine. Even if the internet disconnects, the entire multi-agent system runs flawlessly."*

---

## Slide 11: Live Demonstration Preview
- **Demo Scenario 1: Aspiring Machine Learning Engineer**
  - Background: Beginner Python $\rightarrow$ Target: AI & ML Engineer (12 hrs/week).
  - Results: Stanford ML + Deep Learning Specialization + Fast.ai.
  - Roadmap: 12-week schedule with Neural Network Capstone.
- **Demo Scenario 2: Budget-Constrained Cybersecurity Student**
  - Filter: Free Only $\rightarrow$ Cisco CyberOps + Harvard CS50 + Web Pentesting.

> **Speaker Notes**:
> *"We will now transition to our live demonstration, where we will showcase how EduAgent profiles a student, generates course recommendations, and renders an interactive learning roadmap in real time."*

---

## Slide 12: Conclusion & Q&A
- **Summary**:
  - EduAgent successfully replaces static course lists with an interactive, multi-agent AI curriculum advisor.
  - Blends mathematically sound hybrid information retrieval with explainable agentic workflows.
  - Achieves high recommendation precision ($\text{MRR}=1.0$) with an intuitive, responsive UI.
- **Open for Questions**:
  - Thank you! We welcome questions from the examination committee.

> **Speaker Notes**:
> *"In conclusion, EduAgent demonstrates the power of multi-agent architectures in educational technology. Thank you for your time and attention. I am now open to your questions."*
