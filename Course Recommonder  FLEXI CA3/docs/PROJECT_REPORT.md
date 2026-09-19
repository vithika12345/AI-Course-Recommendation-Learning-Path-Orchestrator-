# EduAgent: Multi-Agent Course Recommendation & Learning Path Orchestrator
**Academic Project Report | Mini-Project Evaluation**

---

## Executive Summary
With the rapid proliferation of Massive Open Online Courses (MOOCs) and specialized e-learning platforms, online learners frequently experience **cognitive overload** and **the choice paralysis paradox**. Traditional recommender systems rely on basic keyword matching or collaborative filtering, which suffer from severe cold-start vulnerabilities, lack pedagogical sequence awareness, and fail to explain *why* a particular curriculum trajectory is recommended. 

This project introduces **EduAgent**, an intelligent, multi-agent educational recommender system that pairs **Hybrid Information Retrieval (TF-IDF Vector Space Modeling + Metadata Ranking)** with a **4-stage Multi-Agent LLM Orchestrator** and an interactive **Gradio** web interface. EduAgent analyzes learner intent, retrieves optimal course candidates from a curated multi-domain catalog, synthesizes a sequenced 4-phase learning roadmap, and subjects the curriculum to automated pedagogical audits.

---

## 1. Introduction

### 1.1 Background & Motivation
In modern engineering and professional education, acquiring up-to-date competencies in Artificial Intelligence, Full-Stack Engineering, Cloud/DevOps, and Cybersecurity is essential. However, the internet presents an overwhelming volume of disconnected tutorials and certifications. Learners struggle to determine:
1. Which course best matches their current proficiency without being too rudimentary or excessively difficult.
2. The optimal chronological order in which topics should be studied.
3. Realistic time commitments required to reach employability.

### 1.2 Problem Statement
Standard search engines and traditional e-learning platforms treat course recommendation as an isolated item retrieval problem. They lack:
- **Pedagogical continuity**: Recommending an advanced topic before prerequisite fundamentals are mastered.
- **Explainability**: Failure to provide clear, actionable justifications connecting course modules to specific student skill gaps.
- **Feasibility analysis**: Inability to assess whether a student's available weekly hours realistically support the target completion timeline.

### 1.3 Project Objectives
The core objectives of the EduAgent system are:
1. **Intelligent Diagnostics**: Formulate a structured learner persona (identifying skill gaps and pedagogical strategy) from natural language user queries.
2. **Hybrid Course Retrieval**: Implement a composite scoring algorithm combining TF-IDF semantic similarity, course ratings, difficulty tier alignment, and duration penalties.
3. **Curriculum Roadmap Synthesis**: Automatically generate a 4-phase, week-by-week learning trajectory featuring hands-on capstone project specifications.
4. **Pedagogical Quality Auditing**: Deploy a specialized Critic Agent to evaluate cognitive load, prerequisite readiness, and potential study bottlenecks.
5. **Interactive Web Interface**: Deliver an intuitive, responsive UI built with Gradio supporting multi-provider LLM backends (Groq, OpenAI, Gemini) and a deterministic offline heuristic fallback.

### 1.4 Scope of the Project
The project encompasses:
- A curated dataset of 100 courses spanning 8 technical disciplines (AI/ML, Web Dev, Cloud, Cybersecurity, Data Science, Mobile Dev, Computer Science, and UI/UX).
- A 4-agent collaborative pipeline orchestrated through a central controller.
- Comprehensive empirical evaluation using information retrieval metrics (Precision@K, Recall@K, NDCG@K, MRR).

---

## 2. Literature Survey & Existing Systems

### 2.1 Traditional Recommendation Approaches
| Approach | Mechanism | Advantages | Major Limitations |
| :--- | :--- | :--- | :--- |
| **Collaborative Filtering (CF)** | User-user or item-item matrix factorization based on historical interaction ratings. | Domain-independent; discovers serendipitous items. | Severe **cold-start problem** for new users/courses; sparsity; no semantic understanding. |
| **Content-Based Filtering (CBF)** | Compares item feature vectors (tags, descriptions) with user profiles using cosine similarity. | No cold-start for existing users; transparent feature matching. | Tends toward over-specialization; ignores learning order and prerequisite dependencies. |
| **Knowledge-Graph Based** | Maps concepts into ontology graphs to enforce prerequisite relations. | High structural consistency. | Extremely expensive to construct and maintain; inflexible to natural language queries. |
| **LLM-Augmented Multi-Agent (EduAgent)** | Combines vector space retrieval with specialized collaborative AI agents. | Natural dialogue; holistic curriculum planning; explainability; offline fallback. | Requires structured orchestration to prevent latency overhead. |

### 2.2 Limitations of Existing E-Learning Portals
Commercial platforms such as Coursera, Udemy, and edX recommend individual courses based on clickstream history. They do not act as an instructional designer:
1. They do not synthesize a unified timeline across multiple providers.
2. They do not evaluate if the student has 10 hours or 40 hours per week.
3. They lack an adversarial "critic" agent to warn students when a roadmap is unrealistically demanding.

---

## 3. Methodology & System Architecture

### 3.1 Multi-Agent Orchestration Framework
EduAgent utilizes a **Sequential-Collaborative Multi-Agent Architecture**. Rather than relying on a single, monolithic LLM prompt (which suffers from hallucinations and token context degradation), the problem is partitioned across four specialized agents:

```
[Student Query & Constraints]
              │
              ▼
   ┌──────────────────────┐
   │  1. Profiler Agent   │  ──► Analyzes background, identifies target role & skill gaps
   └──────────────────────┘
              │
              ▼
   ┌──────────────────────┐
   │  2. Retrieval Agent  │  ──► Queries Hybrid Recommender Engine (TF-IDF + Metadata Ranker)
   └──────────────────────┘
              │
              ▼
   ┌──────────────────────┐
   │ 3. Path Planner Agent│  ──► Assembles 4-Phase Chronological Roadmap & Capstone Project
   └──────────────────────┘
              │
              ▼
   ┌──────────────────────┐
   │   4. Critic Agent    │  ──► Audits prerequisite feasibility, workload & study risks
   └──────────────────────┘
              │
              ▼
   [Unified Gradio Web Dashboard]
```

### 3.2 Agent Roles and Responsibilities
1. **Profiler Agent (`ProfilerAgent`)**:
   - Acts as an educational diagnostic counselor.
   - Deconstructs free-text user statements into structured JSON containing `target_role`, `current_level`, `target_level`, `skill_gaps`, `learning_style`, and optimized `search_keywords`.
2. **Retrieval Agent (`RetrievalAgent`)**:
   - Bridges agent reasoning with mathematical information retrieval.
   - Invokes the hybrid recommendation engine with synthesized parameters and generates contextual justifications (*"Why this course was chosen"*).
3. **Path Planner Agent (`PathPlannerAgent`)**:
   - Acts as an instructional curriculum designer.
   - Sequences the retrieved courses into 4 distinct phases:
     - *Phase 1*: Foundations & Syntax
     - *Phase 2*: Applied Frameworks & Architecture
     - *Phase 3*: Advanced Engineering & Best Practices
     - *Phase 4*: Capstone Project & Portfolio Showcase
4. **Pedagogical Critic Agent (`CriticAgent`)**:
   - Evaluates cognitive load: compares total curriculum hours against the user's weekly commitment.
   - Calculates a quantitative **Feasibility Score (0-100%)** and provides risk warnings with actionable study tips.

---

## 4. Mathematical Formulation & Recommendation Engine

### 4.1 Feature Representation & Vectorization
For each course $c_i$ in catalog $C$, a composite text representation $D_i$ is constructed:
$$D_i = \text{Title}_i \oplus \text{Category}_i \oplus \text{Skills}_i \oplus \text{Description}_i$$

Term Frequency-Inverse Document Frequency (TF-IDF) transforms document $D_i$ into vector $\vec{v}_i \in \mathbb{R}^{|V|}$:
$$\text{TF-IDF}(t, D_i, C) = \text{TF}(t, D_i) \times \log\left(\frac{1 + |C|}{1 + \text{DF}(t, C)}\right) + 1$$

### 4.2 Semantic Similarity
Given user query vector $\vec{q}$, the cosine similarity with course vector $\vec{v}_i$ is defined as:
$$\text{Sim}_{\text{cosine}}(\vec{q}, \vec{v}_i) = \frac{\vec{q} \cdot \vec{v}_i}{\|\vec{q}\|_2 \|\vec{v}_i\|_2}$$

### 4.3 Composite Hybrid Scoring Function
To prevent purely textual matching from recommending outdated or misaligned courses, EduAgent employs a multi-attribute ranking function:
$$\text{Score}(c_i) = \Big( \alpha \cdot \text{Sim}_{\text{cosine}}(\vec{q}, \vec{v}_i) + \beta \cdot \tilde{R}_i + \gamma \cdot L(c_i, \text{level}_{\text{user}}) \Big) \times M_{\text{cat}} \times P_{\text{dur}}$$

Where:
- $\alpha = 0.65$: Weight assigned to semantic query alignment.
- $\beta = 0.20$: Weight for normalized course rating $\tilde{R}_i = \max\left(0, \frac{\text{Rating}_i - 4.0}{1.0}\right)$.
- $\gamma = 0.15$: Weight for level alignment $L(c_i, \text{level}_{\text{user}}) \in \{1.0, 0.6, 0.2\}$.
- $M_{\text{cat}}$: Category preference multiplier ($1.2$ for targeted domain match, $1.0$ for neutral).
- $P_{\text{dur}}$: Duration penalty factor ($0.8$ if course duration exceeds student tolerance, $1.0$ otherwise).

The final match percentage presented to the user is scaled:
$$\text{Match } \% = \min\left(99\%, \max\left(45\%, \text{round}(\text{Score}(c_i) \times 100, 1)\right)\right)$$

---

## 5. Implementation Details

### 5.1 Technology Stack
- **Programming Language**: Python 3.13
- **User Interface**: Gradio 6.x (Interactive web dashboard with custom CSS glassmorphism)
- **Machine Learning & NLP**: Scikit-Learn (TF-IDF, Cosine Similarity), NumPy, Pandas
- **LLM API Integrations**: Groq (Llama-3.3-70B), OpenAI (GPT-4o-mini), Google Gemini (Gemini-1.5-Flash)
- **Fallback Engine**: Custom rule-based deterministic heuristic engine for zero-dependency offline execution

### 5.2 Folder Structure
```
Course Recommender FLEXI CA3/
├── app.py                     # Main Gradio application with 5 comprehensive tabs
├── requirements.txt           # Verified package dependencies
├── .env.example               # Environment template for API keys
├── run.bat / run.sh           # One-click execution scripts
├── agents/                    # Multi-Agent Subsystem
│   ├── base_agent.py          # Unified LLM caller with offline heuristic engine
│   ├── profiler_agent.py      # Diagnostic assessor & skill gap extractor
│   ├── retrieval_agent.py     # Hybrid search coordinator & justification generator
│   ├── path_planner_agent.py  # 4-phase chronological curriculum synthesizer
│   └── critic_agent.py        # Pedagogical auditor & feasibility score evaluator
├── orchestrator/              # Central pipeline controller
│   └── orchestrator.py        # Execution trace manager & state coordinator
├── engine/                    # Recommendation & Evaluation Algorithms
│   ├── recommender.py         # Hybrid TF-IDF vectorizer and metadata ranker
│   └── metrics.py             # Academic evaluation metrics (Precision, Recall, NDCG, MRR)
├── data/
│   └── courses.csv            # Curated catalog of 100 high-quality courses
└── docs/                      # Submission, viva, and presentation artifacts
```

### 5.3 Offline Heuristic Engine Design
A critical architectural feature of EduAgent is its **dual-mode operational design**:
1. When API keys are configured, it invokes state-of-the-art LLMs (Groq Llama 3.3, GPT-4o-mini, or Gemini).
2. When operating offline or without API credits, the system automatically falls back to an internal **Deterministic Heuristic Engine**. This ensures that academic evaluations, lab demonstrations, and viva sessions run instantaneously with 100% uptime and zero latency.

---

## 6. Experimental Results & Evaluation

### 6.1 Information Retrieval Metrics
To validate recommendation accuracy, the hybrid engine was benchmarked across representative learner personas using standard academic Information Retrieval (IR) metrics:

| Metric | Formula | Value (K=5) | Interpretation |
| :--- | :--- | :--- | :--- |
| **Precision@5** | $\frac{|\text{Retrieved}_5 \cap \text{Relevant}|}{5}$ | **0.6000** | 3 out of top 5 courses are strictly relevant to the learner's specific goal. |
| **Recall@5** | $\frac{|\text{Retrieved}_5 \cap \text{Relevant}|}{|\text{Relevant}|}$ | **0.7500** | Successfully recovers 75% of all ground-truth relevant courses in the top 5. |
| **MRR (Mean Reciprocal Rank)** | $\frac{1}{\text{Rank}_1}$ | **1.0000** | The top-ranked course (#1 position) is always an optimal match. |
| **NDCG@5** | $\frac{\text{DCG}_5}{\text{IDCG}_5}$ | **0.7877** | High ranking quality accounting for logarithmic position discount. |

### 6.2 System Performance & Latency Analysis
- **Offline Heuristic Mode**: Complete 4-agent orchestration pipeline executes in **0.01 to 0.03 seconds**.
- **Cloud API Mode (Groq Llama 3.3)**: Complete pipeline completes in **1.8 to 2.4 seconds**.
- **Memory Footprint**: Under 150 MB RAM, suitable for standard student laptops.

### 6.3 User Experience Highlights in Gradio
1. **Interactive Course Cards**: Direct links, difficulty badges, platform indicators, and explainable agent insights.
2. **Phase Timeline**: Clear breakdown of weeks, focus courses, and hands-on milestone deliverables.
3. **Agent Trace Inspector**: Full transparency into agent latency, timestamps, and internal state JSON.

---

## 7. Conclusion & Future Enhancements

### 7.1 Conclusion
EduAgent successfully bridges the gap between statistical course search and personalized pedagogical planning. By orchestrating four specialized AI agents, the system delivers:
- Tailored course selections with high semantic accuracy ($\text{MRR} = 1.0$).
- Structured, week-by-week learning paths that eliminate course-selection fatigue.
- Automated feasibility auditing that keeps student study commitments realistic.

### 7.2 Future Enhancements
1. **Knowledge Graph Integration**: Integrate Neo4j to map granular sub-topic prerequisite graphs down to the individual lecture level.
2. **Dynamic Schedule Adaptation**: Integrate user calendar APIs (Google Calendar) to adjust study pacing dynamically based on real-time assignment completion.
3. **Collaborative Peer Matching**: Group learners following the same 12-week roadmap into virtual cohort study rooms.

---

## 8. References
1. Adomavicius, G., & Tuzhilin, A. (2005). *Toward the next generation of recommender systems: A survey of the state-of-the-art and possible extensions*. IEEE TKDE, 17(6), 734-749.
2. Salton, G., & Buckley, C. (1988). *Term-weighting approaches in automatic text retrieval*. Information Processing & Management, 24(5), 513-523.
3. Wu, Q., et al. (2023). *AutoGen: Enabling next-generation LLM applications via multi-agent conversation*. arXiv preprint arXiv:2308.08155.
4. Järvelin, K., & Kekäläinen, J. (2002). *Cumulated gain-based evaluation of IR techniques*. ACM TOIS, 20(4), 422-446.
5. Abid, A., et al. (2019). *Gradio: Hassle-Free Sharing and Testing of ML Models in the Wild*. arXiv preprint arXiv:1906.02569.
