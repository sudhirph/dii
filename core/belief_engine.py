from typing import List, Tuple

from core.proposals import ForecastProposal


def aggregate_proposals(proposals: List[ForecastProposal]) -> Tuple[float, str]:
    """Aggregate forecast proposals into a single probability and confidence.
    
    Args:
        proposals: List of ForecastProposal objects to aggregate
        
    Returns:
        Tuple of (probability, confidence) where:
        - probability: Average of proposed_probability values
        - confidence: "high", "medium", or "low" based on proposal count
    """
    if not proposals:
        return (0.0, "low")
    
    # Compute average probability
    total_probability = sum(proposal.proposed_probability for proposal in proposals)
    average_probability = total_probability / len(proposals)
    
    # Determine confidence based on proposal count
    if len(proposals) >= 2:
        confidence = "high"
    elif len(proposals) == 1:
        confidence = "medium"
    else:
        confidence = "low"
    
    return (average_probability, confidence)

