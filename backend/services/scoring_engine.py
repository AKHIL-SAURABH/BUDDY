def calculate_final_skill_score(
    concept_score: float, 
    practical_score: float, 
    consistency_score: float, 
    confidence_penalty: float = 1.0
) -> int:
    """
    Calculates the final score for a skill based on the predetermined algorithm.
    Weights: 40% Concept, 30% Practical, 20% Consistency, 10% Confidence.
    """
    
    # Apply standard weights
    weighted_concept = concept_score * 0.40
    weighted_practical = practical_score * 0.30
    weighted_consistency = consistency_score * 0.20
    
    # Confidence is represented as a multiplier (e.g., 0.9 if hesitant, 1.0 if confident)
    # This leaves 10% of the score heavily influenced by the delivery/confidence metric
    base_score = weighted_concept + weighted_practical + weighted_consistency
    final_score = base_score * confidence_penalty
    
    # Ensure score stays within 0-100 bounds
    return max(0, min(100, int(final_score)))

def analyze_gap(required_level: int, actual_score: int) -> str:
    """Returns a categorical gap label for the frontend heatmap."""
    gap = required_level - actual_score
    if gap <= 0:
        return "Strong"
    elif gap <= 20:
        return "Moderate"
    elif gap <= 50:
        return "Weak"
    else:
        return "Missing"