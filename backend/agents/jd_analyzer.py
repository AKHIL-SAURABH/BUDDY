import json
from backend.db.models import JobDescriptionData
from backend.core.config import groq_client

async def analyze_jd(jd_text: str) -> JobDescriptionData:
    """Analyzes a raw Job Description and returns structured requirements."""
    
    schema_str = json.dumps(JobDescriptionData.model_json_schema())
    system_instruction = (
        "You are an expert technical recruiter AI. Your job is to extract the exact technical requirements, skills, and tools from the provided Job Description. Do not hallucinate requirements that are not mentioned.\n\n"
        f"You must respond in valid JSON that perfectly matches this schema:\n{schema_str}"
    )

    response = await groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Extract the data from this Job Description:\n\n{jd_text}"}
        ],
        response_format={"type": "json_object"},
        temperature=0.0
    )
    
    data = json.loads(response.choices[0].message.content)
    return JobDescriptionData(**data)