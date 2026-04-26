# BUDDY: AI-Powered Skill Assessment & Personalised Learning Plan Agent
<p align="center">
  <img src="https://github.com/AKHIL-SAURABH/BUDDY/blob/main/Screenshots/Gemini_Generated_Image_eoe9rheoe9rheoe9.png" 
       alt="Banner Image" 
       width="400"/>
</p>

## Live Links

To use the project, please ensure you start both services (if running locally) or interact with the deployed frontend which communicates with the deployed backend.

- Frontend URL: https://catalyst-frontend-fja2.onrender.com
- Backend URL: https://catalyst-backend-a5tr.onrender.com

---

## Problem Statement

A resume tells you what someone claims to know -- not how well they actually know it. The challenge is to build an agent that takes a Job Description and a candidate's resume, conversationally assesses real proficiency on each required skill, identifies gaps, and generates a personalised learning plan focused on adjacent skills the candidate can realistically acquire -- with curated resources and time estimates.

---

## Solution

BUDDY solves this problem by providing an end-to-end multi-agent pipeline. Instead of relying purely on keyword matching, BUDDY parses the Job Description and Resume to generate a baseline skill map. It then conducts a dynamic, conversational technical interview to empirically test the candidate's proficiency. Finally, it uses the assessment data to pinpoint skill gaps and queries a local vector store to generate a highly personalised, week-by-week learning roadmap with curated resources to help the candidate upskill for the target role.

---

## 🎥 Demo Video

https://github.com/AKHIL-SAURABH/BUDDY/raw/main/Screenshots/demo.mp4

---

## Tech Stack

- Frontend: Streamlit, Plotly (for data visualization)
- Backend: FastAPI, Python
- AI/LLM: Groq API (llama-3.3-70b-versatile)
- Vector Store / Embeddings: FAISS, SentenceTransformers (all-MiniLM-L6-v2)
- Data Validation: Pydantic

---

## Architecture & Project Phases

### Phase 1: Ingestion and Orchestration
The system accepts a Job Description (text) and a Resume (PDF). It leverages asynchronous execution to analyze both documents in parallel, ensuring a fast user experience.

![Upload Interface](https://github.com/AKHIL-SAURABH/BUDDY/blob/main/Screenshots/Screenshot%202026-04-26%20002031.jpg)

Key Code: Orchestrator Pipeline (`backend/agents/orchestrator.py`)
```python
async def process_initial_upload(jd_text: str, resume_pdf_bytes: bytes) -> dict:
    # Extract text from the PDF
    resume_text = extract_text_from_pdf(resume_pdf_bytes)
    
    # Run JD and Resume analysis IN PARALLEL for maximum speed
    jd_data, resume_data = await asyncio.gather(
        analyze_jd(jd_text),
        analyze_resume(resume_text)
    )
    
    # Pass the results to the Skill Mapper
    skill_mapping = await map_skills(jd_data, resume_data)
    
    return {
        "jd_data": jd_data.model_dump(),
        "resume_data": resume_data.model_dump(),
        "skill_mapping": skill_mapping.model_dump()
    }
```
**Functionality:** This function orchestrates the first major workflow. It parses the PDF, concurrently queries the LLM to extract structured data from both the JD and the resume, and then maps the candidate's skills to the JD's requirements to identify matched, missing, and adjacent skills.

### Phase 2: Pre-Assessment Analysis
Before jumping into an interview, the user is presented with a summary of their baseline skill match based purely on document analysis.

![Pre-Assessment Summary Page](https://github.com/AKHIL-SAURABH/BUDDY/blob/main/Screenshots/Screenshot%202026-04-26%20002144.jpg)

Key Code: Skill Mapper Agent (`backend/agents/skill_mapper.py`)
```python
async def map_skills(jd_data: JobDescriptionData, resume_data: CandidateCapabilities) -> SkillGraphMapping:
    context = f"""
    Job Requirements: {jd_data.skills}
    Candidate Skills: {list(resume_data.skills.keys())}
    """
    
    response = await groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": context}
        ],
        response_format={"type": "json_object"}
    )
    return SkillGraphMapping(**json.loads(response.choices[0].message.content))
```
**Functionality:** The skill mapper agent compares the extracted candidate skills against the job requirements and categorizes them. This powers the visual summary page where users see their JD Match Strength percentage before beginning the live assessment.

### Phase 3: Conversational Assessment
BUDDY acts as a technical interviewer, dynamically generating questions based on the skill being tested and adjusting difficulty based on the candidate's previous answers.

![Live Interview Chat Interface](https://github.com/AKHIL-SAURABH/BUDDY/blob/main/Screenshots/Screenshot%202026-04-26%20002458.jpg)


Key Code: Assessment Agent (`backend/agents/assessment_agent.py`)
```python
    if not previous_question:
        context = f"This is the first question for the skill: {skill}. Start with a {current_difficulty} difficulty conceptual question."
    else:
        context = f"""
        Skill being tested: {skill}
        Previous Question: {previous_question}
        Candidate's Answer: {candidate_answer}
        
        Task: 
        1. Evaluate the answer strictly out of 100.
        2. If the score is > 75, increase the difficulty for the next question.
        3. If the score is < 40, decrease the difficulty to Basic.
        4. If you have asked at least 3 questions and have a confident read on their ability, set 'is_completed' to True.
        5. Don't ask more than 6 questions in total.
        """
```
**Functionality:** This prompt dictates the state machine of the interview. The agent evaluates the user's answer, scores it, dictates the next difficulty level, and decides whether enough data has been collected to terminate the assessment (capped at 6 questions).

### Phase 4: Results & Personalised Learning Plan
Once the assessment concludes, BUDDY generates a visual gap analysis using the tracked scores and queried a FAISS vector database to build a tailored learning roadmap.

![Gap Analysis Chart](https://github.com/AKHIL-SAURABH/BUDDY/blob/main/Screenshots/Screenshot%202026-04-26%20002526.jpg)

![Skill Gap Analysis](https://github.com/AKHIL-SAURABH/BUDDY/blob/main/Screenshots/Screenshot%202026-04-26%20002542.jpg)



Key Code: Vector Store Lazy Loading (`backend/services/vector_store.py`)
```python
class ResourceVectorStore:
    def __init__(self):
        self._encoder = None
        self.dimension = 384
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata_store = []

    @property
    def encoder(self):
        if self._encoder is None:
            from sentence_transformers import SentenceTransformer
            self._encoder = SentenceTransformer('all-MiniLM-L6-v2')
        return self._encoder
```
**Functionality:** Because embedding models are heavy, the `SentenceTransformer` is lazy-loaded. This ensures the backend boots instantly upon deployment without timing out, only downloading and loading the model into memory when a roadmap actually needs to be generated.

![Learning Roadmap](https://github.com/AKHIL-SAURABH/BUDDY/blob/main/Screenshots/Screenshot%202026-04-26%20002601.jpg)


Key Code: Roadmap Generation (`backend/agents/learning_planner.py`)
```python
async def generate_learning_roadmap(target_role: str, gap_data: GapAnalysisResult) -> LearningRoadmap:
    all_gaps = gap_data.weak + gap_data.missing
    resources = []
    
    for gap in all_gaps:
        found = resource_db.retrieve_resources(gap, top_k=2)
        resources.extend(found)
        
    context = f"""
    Target Role: {target_role}
    Critical Gaps: {all_gaps}
    Available Curated Resources: {resources}
    """
    # ... calls the Groq API to format the weekly plan
```
**Functionality:** The learning planner takes the weak and missing skills identified during the assessment, queries the local FAISS index for relevant learning materials, and instructs the LLM to structure a realistic, week-by-week study plan utilizing those specific resources.
