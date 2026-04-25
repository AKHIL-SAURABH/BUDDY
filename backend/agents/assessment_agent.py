import json
from backend.db.models import AssessmentTurn
from backend.core.config import groq_client

async def execute_interview_turn(
    skill: str, 
    previous_question: str = None, 
    candidate_answer: str = None, 
    current_difficulty: str = "Medium"
) -> AssessmentTurn:
    """Evaluates the candidate's answer and generates the next adaptive question."""
    
    schema_str = json.dumps(AssessmentTurn.model_json_schema())
    system_instruction = (
        "You are a senior technical interviewer. Ask highly specific, practical questions. Do not ask generic trivia.\n\n"
        f"You must respond in valid JSON that perfectly matches this schema:\n{schema_str}"
    )
    
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
        5. Don't ask more than 6 questions in total. Set 'is_completed' to True if you reach 6 questions.
        """

    response = await groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": context}
        ],
        response_format={"type": "json_object"},
        temperature=0.7
    )
    
    data = json.loads(response.choices[0].message.content)
    return AssessmentTurn(**data)