from typing import List

from core.alerts import AlertCandidate


def build_alerts(changes: List[dict], beliefs: List[dict]) -> List[AlertCandidate]:
    """Build alert candidates from changes and beliefs.
    
    Args:
        changes: List of change dicts from /portfolio/changes endpoint
        beliefs: List of belief dicts with entity_id and confidence
        
    Returns:
        List of AlertCandidate objects sorted by priority_rank ascending, limited to top 10
    """
    # Create a lookup for beliefs by entity_id
    belief_lookup = {belief["entity_id"]: belief for belief in beliefs}
    
    alert_candidates = []
    
    for change in changes:
        entity_id = change["entity_id"]
        event_id = "NEXT_ROUND_RAISED"  # From the changes endpoint
        
        # Get confidence from beliefs
        belief = belief_lookup.get(entity_id, {})
        confidence = belief.get("confidence", "low")
        
        # Assign priority_rank based on rules
        # Lower rank = higher priority
        priority_rank = _calculate_priority_rank(
            change["change_type"],
            change["probability"],
            change.get("delta"),
            confidence,
        )
        
        # Assign human-readable reason
        reason = _generate_reason(
            change["change_type"],
            change["probability"],
            change.get("delta"),
            confidence,
        )
        
        alert_candidates.append(
            AlertCandidate(
                entity_id=entity_id,
                event_id=event_id,
                probability=change["probability"],
                delta=change.get("delta"),
                change_type=change["change_type"],
                confidence=confidence,
                priority_rank=priority_rank,
                reason=reason,
                as_of=change["as_of"],
            )
        )
    
    # Sort by priority_rank ascending (lower rank = higher priority)
    alert_candidates.sort(key=lambda x: x.priority_rank)
    
    # Limit to top 10
    return alert_candidates[:10]


def _calculate_priority_rank(
    change_type: str, probability: float, delta: float | None, confidence: str
) -> int:
    """Calculate priority rank. Lower rank = higher priority.
    
    Priority rules:
    - significant_drop: highest priority (rank 1-3)
    - significant_rise: medium priority (rank 4-6)
    - initial: lowest priority (rank 7-9)
    - Within each type, lower probability = higher priority
    - Higher confidence = higher priority (lower rank)
    """
    base_rank = {
        "significant_drop": 1,
        "significant_rise": 4,
        "initial": 7,
    }.get(change_type, 10)
    
    # Adjust for probability (lower probability = higher priority)
    probability_adjustment = int((1.0 - probability) * 2)  # 0-2 points
    
    # Adjust for confidence (high=0, medium=1, low=2)
    confidence_adjustment = {"high": 0, "medium": 1, "low": 2}.get(confidence, 2)
    
    return base_rank + probability_adjustment + confidence_adjustment


def _generate_reason(
    change_type: str, probability: float, delta: float | None, confidence: str
) -> str:
    """Generate human-readable reason for the alert."""
    prob_pct = f"{probability * 100:.1f}%"
    
    if change_type == "significant_drop":
        delta_pct = f"{abs(delta) * 100:.1f}%" if delta is not None else "N/A"
        return f"Significant drop of {delta_pct} in probability to {prob_pct} ({confidence} confidence)"
    elif change_type == "significant_rise":
        delta_pct = f"{delta * 100:.1f}%" if delta is not None else "N/A"
        return f"Significant rise of {delta_pct} in probability to {prob_pct} ({confidence} confidence)"
    elif change_type == "initial":
        return f"Initial belief established at {prob_pct} ({confidence} confidence)"
    else:
        return f"Change detected: {change_type} to {prob_pct} ({confidence} confidence)"

