import json
from backend.db.models import CandidateCapabilities
from backend.core.config import groq_client

async def analyze_resume(resume_text: str) -> CandidateCapabilities:
    """Analyzes a candidate's resume to establish their baseline capabilities."""
    
    schema_str = json.dumps(CandidateCapabilities.model_json_schema())
    system_instruction = (
        "You are a highly analytical technical evaluator AI. Extract the candidate's technical skills, map their perceived proficiency (None, Basic, Intermediate, Advanced, Expert), summarize key projects, and calculate total years of relevant experience from the provided resume text.\n\n"
        f"You must respond in valid JSON that perfectly matches this schema:\n{schema_str}"
    )

    response = await groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Analyze this resume:\n\n{resume_text}"}
        ],
        response_format={"type": "json_object"},
        temperature=0.0
    )
    
    data = json.loads(response.choices[0].message.content)
    return CandidateCapabilities(**data)