from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.agents.assessment_agent import execute_interview_turn

router = APIRouter()

# We define a quick Pydantic schema for the incoming chat request
class ChatTurnRequest(BaseModel):
    skill: str
    previous_question: Optional[str] = None
    candidate_answer: Optional[str] = None
    current_difficulty: str = "Medium"

@router.post("/chat-turn")
async def handle_chat_turn(request: ChatTurnRequest):
    """Processes a single turn of the adaptive interview."""
    try:
        turn_result = await execute_interview_turn(
            skill=request.skill,
            previous_question=request.previous_question,
            candidate_answer=request.candidate_answer,
            current_difficulty=request.current_difficulty
        )
        return {"status": "success", "data": turn_result.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))