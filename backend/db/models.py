from pydantic import BaseModel, Field
from typing import List, Dict, Optional

# --- 1. JD Analyzer Models ---
class JobDescriptionData(BaseModel):
    role: str = Field(description="The primary job title")
    skills: List[str] = Field(description="List of required core skills")
    experience_level: str = Field(description="Required experience level (e.g., Entry, Intermediate, Senior)")
    tools: List[str] = Field(description="Specific software or tools required")

# --- 2. Resume Analyzer Models ---
class CandidateCapabilities(BaseModel):
    skills: Dict[str, str] = Field(description="Dictionary of skills and their perceived depth (e.g., {'Python': 'Intermediate'})")
    projects: List[str] = Field(description="Brief summaries of relevant projects found on the resume")
    experience_years: float = Field(description="Total years of relevant experience")

# --- 3. Skill Mapping & Gap Analysis Models ---
class SkillGraphMapping(BaseModel):
    matched_skills: List[str]
    missing_skills: List[str]
    adjacent_skills: List[str]

class GapAnalysisResult(BaseModel):
    strong: List[str]
    moderate: List[str]
    weak: List[str]
    missing: List[str]

class SkillScores(BaseModel):
    scores: Dict[str, int] = Field(description="Dictionary mapping skill names to their calculated score out of 100")

# --- 4. Learning Plan Models ---
class Resource(BaseModel):
    title: str
    url: Optional[str]
    type: str = Field(description="e.g., 'Course', 'Documentation', 'Project'")

class WeeklyPlan(BaseModel):
    week: int
    focus: str
    resources: List[Resource]
    hours: int

class LearningRoadmap(BaseModel):
    target_role: str
    plan: List[WeeklyPlan]

# --- Add to backend/db/models.py ---

class AssessmentTurn(BaseModel):
    is_completed: bool = Field(description="True if the agent has gathered enough data to confidently score the skill, False to keep asking.")
    evaluation_score: Optional[int] = Field(description="Score from 0-100 of the candidate's previous answer. Null if this is the first question.")
    evaluation_reasoning: Optional[str] = Field(description="Brief internal logic on why this score was given.")
    next_difficulty: Optional[str] = Field(description="Difficulty for the next question: Basic, Intermediate, or Advanced. Null if is_completed is True.")
    next_question: Optional[str] = Field(description="The next technical question to ask the candidate. Null if is_completed is True.")