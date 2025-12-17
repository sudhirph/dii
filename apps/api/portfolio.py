from fastapi import APIRouter

from core.belief_store import get_distinct_entity_ids, get_latest_belief, get_previous_belief

router = APIRouter()


@router.get("/portfolio/overview")
def get_portfolio_overview():
    """Get portfolio overview for NEXT_ROUND_RAISED event.
    
    Returns:
        List of portfolio items with: entity_id, probability, confidence, delta, risk_level, as_of
    """
    event_id = "NEXT_ROUND_RAISED"
    
    # Get all distinct entity_ids
    entity_ids = get_distinct_entity_ids(event_id)
    
    portfolio_items = []
    
    for entity_id in entity_ids:
        # Fetch latest belief
        current_belief = get_latest_belief(event_id, entity_id)
        if current_belief is None:
            continue
        
        # Fetch previous belief
        previous_belief = get_previous_belief(event_id, entity_id)
        
        # Compute delta
        if previous_belief is not None:
            delta = current_belief.probability - previous_belief.probability
        else:
            delta = None
        
        # Classify risk
        probability = current_belief.probability
        if probability < 0.4:
            risk_level = "high_risk"
        elif probability < 0.7:
            risk_level = "medium_risk"
        else:
            risk_level = "low_risk"
        
        portfolio_items.append({
            "entity_id": entity_id,
            "probability": probability,
            "confidence": current_belief.confidence,
            "delta": delta,
            "risk_level": risk_level,
            "as_of": current_belief.as_of,
        })
    
    return portfolio_items

