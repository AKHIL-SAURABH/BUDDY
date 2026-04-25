from fastapi import APIRouter, HTTPException
from backend.db.models import GapAnalysisResult
from backend.agents.learning_planner import generate_learning_roadmap

router = APIRouter()

@router.post("/generate-roadmap")
async def generate_roadmap_endpoint(target_role: str, gap_data: GapAnalysisResult):
    """Takes the final gap analysis and generates the week-by-week plan."""
    try:
        roadmap = await generate_learning_roadmap(target_role, gap_data)
        return {"status": "success", "data": roadmap.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))