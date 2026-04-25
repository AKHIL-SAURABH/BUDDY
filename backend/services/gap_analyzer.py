from backend.db.models import GapAnalysisResult
from typing import Dict, List

def compute_skill_gaps(required_skills: List[str], evaluated_scores: Dict[str, int]) -> GapAnalysisResult:
    """
    Compares the required skills from the JD against the candidate's actual evaluated scores.
    Categorizes them into Strong, Moderate, Weak, or Missing for the frontend dashboard.
    """
    analysis = {
        "strong": [],
        "moderate": [],
        "weak": [],
        "missing": []
    }

    for skill in required_skills:
        # If the skill wasn't evaluated or the candidate didn't have it at all
        if skill not in evaluated_scores:
            analysis["missing"].append(skill)
        else:
            score = evaluated_scores[skill]
            
            # Thresholding logic
            if score >= 80:
                analysis["strong"].append(skill)
            elif score >= 50:
                analysis["moderate"].append(skill)
            else:
                analysis["weak"].append(skill)

    # Return the validated Pydantic model
    return GapAnalysisResult(**analysis)