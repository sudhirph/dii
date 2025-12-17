from fastapi import APIRouter

from core.alert_builder import build_alerts
from core.belief_store import get_latest_belief
from core.change_detector import detect_belief_change
from core.portfolio_store import get_entities_with_beliefs, get_previous_belief

router = APIRouter()


@router.get("/portfolio/alerts")
def get_portfolio_alerts():
    """Get portfolio alerts for NEXT_ROUND_RAISED event.
    
    Returns:
        List of alert candidates ordered by priority, with fields:
        entity_id, probability, delta, change_type, confidence, reason, as_of
    """
    event_id = "NEXT_ROUND_RAISED"
    
    # Get all entities with beliefs
    entity_ids = get_entities_with_beliefs(event_id)
    
    changes = []
    beliefs = []
    
    for entity_id in entity_ids:
        # Fetch latest belief
        current_belief = get_latest_belief(event_id, entity_id)
        if current_belief is None:
            continue
        
        # Fetch previous belief
        previous_belief = get_previous_belief(
            event_id, entity_id, current_belief.belief_id
        )
        
        # Detect change
        change_info = detect_belief_change(current_belief, previous_belief)
        
        # Only include if change_type is not "no_material_change"
        if change_info["change_type"] != "no_material_change":
            changes.append({
                "entity_id": entity_id,
                "probability": current_belief.probability,
                "delta": change_info["delta"],
                "change_type": change_info["change_type"],
                "as_of": current_belief.as_of,
            })
        
        # Add belief data for enrichment
        beliefs.append({
            "entity_id": entity_id,
            "confidence": current_belief.confidence,
        })
    
    # Build alert candidates
    alert_candidates = build_alerts(changes, beliefs)
    
    # Return specified fields
    return [
        {
            "entity_id": alert.entity_id,
            "probability": alert.probability,
            "delta": alert.delta,
            "change_type": alert.change_type,
            "confidence": alert.confidence,
            "reason": alert.reason,
            "as_of": alert.as_of,
        }
        for alert in alert_candidates
    ]

