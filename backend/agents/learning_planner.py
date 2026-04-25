import json
from backend.db.models import GapAnalysisResult, LearningRoadmap
from backend.services.vector_store import resource_db
from backend.core.config import groq_client

async def generate_learning_roadmap(
    target_role: str, 
    gap_analysis: GapAnalysisResult
) -> LearningRoadmap:
    """Creates a time-boxed learning roadmap based on identified weak/missing skills."""
    
    curated_materials = []
    for skill in gap_analysis.missing + gap_analysis.weak:
        docs = resource_db.retrieve_resources(skill, top_k=2)
        curated_materials.extend(docs)
        
    schema_str = json.dumps(LearningRoadmap.model_json_schema())
    system_instruction = (
        "You are a senior career coach and curriculum designer. Build highly efficient, strictly formatted learning roadmaps.\n\n"
        f"You must respond in valid JSON that perfectly matches this schema:\n{schema_str}"
    )
        
    context = f"""
    Target Role: {target_role}
    Weak Skills: {gap_analysis.weak}
    Missing Skills: {gap_analysis.missing}
    
    Available Curated Resources to use in the plan:
    {curated_materials}
    
    Task: Create a highly specific, week-by-week learning plan prioritizing the Missing and Weak skills. 
    Use the provided Curated Resources. Assign realistic hour estimates per week.
    """

    response = await groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": context}
        ],
        response_format={"type": "json_object"},
        temperature=0.4
    )
    
    data = json.loads(response.choices[0].message.content)
    return LearningRoadmap(**data)