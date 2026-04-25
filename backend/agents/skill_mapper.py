import json
from backend.db.models import (
    JobDescriptionData,
    CandidateCapabilities,
    SkillGraphMapping,
)
from backend.core.config import groq_client


async def map_skills(
    jd_data: JobDescriptionData, resume_data: CandidateCapabilities
) -> SkillGraphMapping:
    """Compares JD requirements against Candidate skills to find gaps and adjacencies."""

    schema_str = json.dumps(SkillGraphMapping.model_json_schema())
    system_instruction = (
        "You are a precise data-mapping AI. Compare Job Requirements with Candidate Capabilities to find matched, missing, and adjacent skills.\n\n"
        f"You must respond in valid JSON that perfectly matches this schema:\n{schema_str}"
    )

    prompt = f"""
    Job Requirements: {jd_data.model_dump_json()}
    Candidate Capabilities: {resume_data.model_dump_json()}
    
    Task:
    1. Identify 'matched_skills' (skills the candidate possesses that the job requires).
    2. Identify 'missing_skills' (critical skills the job requires that the candidate completely lacks).
    3. Identify 'adjacent_skills' (skills the candidate has that are highly transferrable to the missing skills).
    """

    response = await groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
    )

    data = json.loads(response.choices[0].message.content)
    return SkillGraphMapping(**data)
