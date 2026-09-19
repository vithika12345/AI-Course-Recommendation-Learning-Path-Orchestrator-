# EduAgent: Comprehensive Viva Questions & Simple English Answers
**Subject: AI Agent for Course Recommendation | Evaluation Rubric: Viva (5 Marks)**

---

## Quick Reference Summary for the Viva
- **Project Name**: EduAgent: Multi-Agent Course Recommendation & Learning Path Orchestrator
- **Frontend**: Gradio 6.x with custom CSS glassmorphism
- **Backend**: Python 3.13, Scikit-Learn, Pandas, NumPy, Requests
- **Architecture**: Sequential-Collaborative Multi-Agent Architecture (4 Agents)
  1. `ProfilerAgent`: Diagnoses user goals, level, and extracts skill gaps.
  2. `RetrievalAgent`: Coordinates hybrid vector retrieval and writes justifications.
  3. `PathPlannerAgent`: Organizes courses into a 4-phase weekly roadmap with capstones.
  4. `CriticAgent`: Audits prerequisite readiness, calculates feasibility score (0-100%), and gives study tips.
- **Engine**: Hybrid Content-Based Filtering (TF-IDF Cosine Similarity + Metadata Ranker).
- **Supported LLMs**: Groq (Llama 3.3), OpenAI (GPT-4o-mini), Google Gemini (Gemini 1.5 Flash), and an Offline Heuristic Engine.

---

## Category 1: Recommender System Fundamentals

### Q1. What type of recommender system have you implemented?
**Answer**:
"We implemented a **Hybrid Recommender System**. It blends **Content-Based Filtering** using TF-IDF vectorization and Cosine Similarity with **Heuristic Metadata Ranking** (course rating, level matching, price filters, duration penalties), augmented by **LLM-powered Multi-Agent reasoning** to organize the recommendations into a structured curriculum."

### Q2. Why didn't you use pure Collaborative Filtering?
**Answer**:
"Collaborative Filtering requires a massive matrix of past user ratings and clicks. It suffers from the **Cold-Start Problem**—it cannot recommend new courses or help a new student who has no rating history. In contrast, our hybrid approach understands the content and semantic skill tags directly, allowing instant recommendations for any learner from day one."

### Q3. How does TF-IDF work in your recommendation engine?
**Answer**:
"TF-IDF stands for Term Frequency-Inverse Document Frequency.
- **Term Frequency (TF)** measures how often a skill keyword appears in a course's title, description, and syllabus.
- **Inverse Document Frequency (IDF)** lowers the weight of common words (like 'course' or 'learn') and increases the weight of rare, important skills (like 'PyTorch', 'Docker', or 'Kubernetes').
This creates a numerical vector for each course that captures its unique technical identity."

### Q4. What is Cosine Similarity, and why is it used here?
**Answer**:
"Cosine Similarity measures the cosine of the angle between two multi-dimensional vectors—in our case, the user's query vector and each course's vector.
$$\text{Cosine Similarity} = \frac{\vec{A} \cdot \vec{B}}{\|\vec{A}\| \|\vec{B}\|}$$
Its value ranges from 0 to 1. A score close to 1 means the course text aligns closely with the student's learning goals, regardless of description length."

---

## Category 2: Agentic AI & Multi-Agent Orchestration

### Q5. What is an AI Agent, and how is it different from a standard LLM prompt?
**Answer**:
"A standard LLM prompt simply generates a one-shot response to a question. An **AI Agent** is an autonomous entity with a defined **role, goals, memory, and tools**. It can perceive user inputs, reason step-by-step, call external tools (like our retrieval engine), validate its own outputs, and collaborate with other agents to accomplish complex workflows."

### Q6. Why use a Multi-Agent architecture instead of a single prompt?
**Answer**:
"Using a single prompt to do profiling, search, curriculum roadmapping, and quality auditing causes **context dilution and hallucinations**.
By separating the task into four specialized agents:
1. Each agent has a single, focused responsibility.
2. We can inspect the intermediate outputs at each step (explainability).
3. The system is modular: we can update the recommender engine without breaking the roadmap planner."

### Q7. Explain the roles of the 4 agents in your system.
**Answer**:
1. **ProfilerAgent**: Acts as an educational counselor. It extracts the student's current proficiency, target role, weekly hours, and missing skill gaps.
2. **RetrievalAgent**: Takes the search keywords from the Profiler, queries the hybrid search engine, and writes a personalized justification explaining why each course was selected.
3. **PathPlannerAgent**: Acts as an instructional designer. It organizes the courses into a chronological 4-phase roadmap (Foundations $\rightarrow$ Applied Frameworks $\rightarrow$ Advanced Topics $\rightarrow$ Capstone Project).
4. **CriticAgent**: Acts as an academic auditor. It checks if the total hours fit the student's weekly schedule, verifies prerequisites, assigns a **Feasibility Score (0-100%)**, and flags potential study bottlenecks.

### Q8. What is the role of the MultiAgentOrchestrator?
**Answer**:
"The `MultiAgentOrchestrator` is the central controller. It passes shared context between the agents in sequence, measures execution time and latency for each step, handles error recovery, and packages the final result into an explainable trace for the UI."

---

## Category 3: Recommendation Formulas & Evaluation Metrics

### Q9. What is your composite ranking formula?
**Answer**:
"Our hybrid score combines text similarity and metadata:
$$\text{Score} = (\alpha \cdot \text{Sim}_{\text{cosine}} + \beta \cdot \text{Normalized Rating} + \gamma \cdot \text{Level Match}) \times \text{Category Match} \times \text{Duration Penalty}$$
We use $\alpha = 0.65$ for semantic relevance, $\beta = 0.20$ for rating quality, and $\gamma = 0.15$ for difficulty alignment."

### Q10. How did you evaluate your recommender system?
**Answer**:
"We evaluated our system using standard academic Information Retrieval metrics:
- **Precision@5 (0.6000)**: 60% of top 5 recommended items are directly relevant to the target role.
- **Recall@5 (0.7500)**: 75% of all relevant courses in the database were successfully captured in the top 5.
- **Mean Reciprocal Rank (MRR = 1.0000)**: The #1 ranked recommendation is always an optimal match.
- **NDCG@5 (0.7877)**: Normalized Discounted Cumulative Gain proves high ranking quality where more relevant items appear higher on the list."

### Q11. What is NDCG, and why is it important?
**Answer**:
"NDCG stands for **Normalized Discounted Cumulative Gain**. Unlike simple precision, NDCG rewards algorithms for placing the best recommendations at the very top of the list by penalizing relevant items that appear further down using a logarithmic discount factor."

---

## Category 4: Implementation, Gradio & LLM Integrations

### Q12. Why did you choose Gradio for the frontend?
**Answer**:
"Gradio is the industry standard for deploying machine learning and AI applications. It allows rapid prototyping of reactive web components, supports custom CSS styling, handles complex multi-tab layouts natively in Python, and enables effortless live demonstrations during examinations."

### Q13. Which LLMs are supported, and how do you prevent crashes if the internet drops?
**Answer**:
"We support **Groq (Llama 3.3 70B)** for high-speed inference, **OpenAI (GPT-4o-mini)**, and **Google Gemini (Gemini 1.5 Flash)**.
Crucially, we designed an **Intelligent Offline Heuristic Engine**. If no API key is provided or if network connectivity is lost, the system automatically falls back to deterministic rule-based NLP templates. This guarantees that our live viva demonstration **never fails or times out**."

### Q14. Where is your course data stored, and what does it contain?
**Answer**:
"The course catalog is stored in `data/courses.csv`. It contains 100 curated courses across 8 domains (AI/ML, Web Dev, Cloud, CyberSec, Data Science, Mobile Dev, CS, UI/UX). Each course has fields: `course_id`, `title`, `provider`, `category`, `level`, `rating`, `duration_hours`, `price_usd`, `skills_covered`, `prerequisites`, `description`, and `url`."

---

## Category 5: Tough Examiner "Gotcha" Questions & Defenses

### Q15. "What if a beginner student types 'I want to build autonomous self-driving cars in 2 weeks'?"
**Answer**:
"The system handles this gracefully across two agents:
1. **ProfilerAgent** notes that the declared experience is Beginner and derives prerequisite math and Python gaps.
2. **CriticAgent** audits the unrealistic 2-week timeline against the 100+ coursework hours required. It lowers the **Feasibility Score** to ~65%, flags an **'Overloaded / Unrealistic'** workload warning, and explicitly advises the student to extend their timeline to at least 12-16 weeks."

### Q16. "How do you prevent the LLM from hallucinating fake course URLs?"
**Answer**:
"The LLM is **not** allowed to invent courses or URLs. Course retrieval is strictly grounded in our verified `courses.csv` database via the `CourseRecommenderEngine`. The LLMs only generate the diagnostic profile, pedagogical reasoning, and roadmap sequencing around the real courses retrieved."

### Q17. "What is the computational complexity of your search engine?"
**Answer**:
"Building the TF-IDF matrix takes $O(N \cdot L)$ where $N$ is the number of courses (100) and $L$ is average document length.
At query time, vector transforming the query and computing cosine similarity against the sparse matrix is $O(N \cdot |V_{\text{query}}|)$, which executes in less than **10 milliseconds**, ensuring instantaneous response times."

### Q18. "How does your system scale if the catalog grows to 100,000 courses?"
**Answer**:
"For 100,000 courses, we would replace in-memory scikit-learn cosine similarity with an approximate nearest neighbors (ANN) vector database such as **Pinecone, FAISS, or ChromaDB** using dense sentence-transformer embeddings. The multi-agent orchestrator architecture remains identical."

### Q19. "Can a student filter for only free courses?"
**Answer**:
"Yes! The UI has a **Budget Constraint** dropdown with an option for 'Free Only'. When selected, the recommender engine filters out all courses where `price_usd > 0`, returning top-rated free courses from Harvard CS50, Fast.ai, MIT OCW, University of Helsinki, and Google Developers."

### Q20. "What is the single biggest advantage of your project over existing platforms like Coursera or Udemy?"
**Answer**:
"Existing platforms only recommend individual courses to sell them. **EduAgent acts as a personal AI Academic Advisor**: it identifies skill gaps, chains complementary courses across different universities into an organized 12-week roadmap, designs a custom capstone portfolio project, and audits the workload feasibility before the student starts."
