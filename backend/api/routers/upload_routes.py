from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from backend.agents.orchestrator import process_initial_upload

router = APIRouter()

@router.post("/upload")
async def handle_upload(
    jd_text: str = Form(...),
    resume: UploadFile = File(...)
):
    """Ingests the JD and Resume, returning the initial skill mapping."""
    if not resume.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF resumes are supported.")
    
    try:
        # Read the file bytes asynchronously
        file_bytes = await resume.read()
        
        # Trigger the parallel Orchestrator pipeline
        result = await process_initial_upload(jd_text, file_bytes)
        
        return {"status": "success", "data": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))