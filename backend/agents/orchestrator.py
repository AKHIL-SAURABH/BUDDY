import asyncio
from backend.services.pdf_parser import extract_text_from_pdf
from backend.agents.jd_analyzer import analyze_jd
from backend.agents.resume_analyzer import analyze_resume
from backend.agents.skill_mapper import map_skills

async def process_initial_upload(jd_text: str, resume_pdf_bytes: bytes) -> dict:
    """
    Master pipeline for Step 1 through Step 4.
    Ingests files, parses data, and generates the baseline skill map.
    """
    
    # 1. Extract text from the PDF
    resume_text = extract_text_from_pdf(resume_pdf_bytes)
    
    # 2. Run JD and Resume analysis IN PARALLEL for maximum speed
    # This is why we used async Python!
    jd_data, resume_data = await asyncio.gather(
        analyze_jd(jd_text),
        analyze_resume(resume_text)
    )
    
    # 3. Pass the results to the Skill Mapper
    skill_mapping = await map_skills(jd_data, resume_data)
    
    # 4. Return the compiled state to be saved in the database or sent to the frontend
    return {
        "jd_data": jd_data.model_dump(),
        "resume_data": resume_data.model_dump(),
        "skill_mapping": skill_mapping.model_dump()
    }