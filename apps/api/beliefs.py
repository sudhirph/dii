from fastapi import APIRouter, HTTPException, Query

from core.belief_store import get_latest_belief, get_belief_history
from core.proposal_store import get_proposals

router = APIRouter()


@router.get("/beliefs/{event_id}")
def get_belief(event_id: str, entity_id: str = Query(...)):
    """Get the latest belief snapshot for a given event and entity.
    
    Args:
        event_id: The event identifier (path parameter)
        entity_id: The entity identifier (query parameter)
        
    Returns:
        Belief snapshot with: belief_id, event_id, entity_id, probability, confidence, as_of
        
    Raises:
        HTTPException: 404 if no belief found
    """
    belief = get_latest_belief(event_id, entity_id)
    
    if belief is None:
        raise HTTPException(status_code=404, detail="Belief not found")
    
    return {
        "belief_id": belief.belief_id,
        "event_id": belief.event_id,
        "entity_id": belief.entity_id,
        "probability": belief.probability,
        "confidence": belief.confidence,
        "as_of": belief.as_of,
    }


@router.get("/beliefs/{event_id}/history")
def get_belief_history_endpoint(event_id: str, entity_id: str = Query(...)):
    """Get belief history for a given event and entity.
    
    Args:
        event_id: The event identifier (path parameter)
        entity_id: The entity identifier (query parameter)
        
    Returns:
        List of belief snapshots with: belief_id, probability, confidence, as_of
        Ordered by as_of ascending (oldest first), limited to 20 records
    """
    history = get_belief_history(event_id, entity_id, limit=20)
    return history


@router.get("/beliefs/{event_id}/explain")
def explain_belief(event_id: str, entity_id: str = Query(...)):
    """Explain a belief by showing the contributing proposals.
    
    Args:
        event_id: The event identifier (path parameter)
        entity_id: The entity identifier (query parameter)
        
    Returns:
        Explanation with: belief_id, probability, confidence, contributing_agents, rationale
        
    Raises:
        HTTPException: 404 if no belief found
    """
    # Fetch latest belief
    belief = get_latest_belief(event_id, entity_id)
    
    if belief is None:
        raise HTTPException(status_code=404, detail="Belief not found")
    
    # Fetch proposals used to compute the belief
    proposals = get_proposals(event_id, entity_id)
    
    # Build contributing_agents list
    contributing_agents = [
        {
            "agent_id": proposal.agent_id,
            "proposed_probability": proposal.proposed_probability,
        }
        for proposal in proposals
    ]
    
    # Combine rationales from proposals
    rationale = " | ".join(proposal.rationale for proposal in proposals)
    
    return {
        "belief_id": belief.belief_id,
        "probability": belief.probability,
        "confidence": belief.confidence,
        "contributing_agents": contributing_agents,
        "rationale": rationale,
    }

