from fastapi import APIRouter, HTTPException, Query

from core.belief_store import get_latest_belief, get_belief_history
from core.proposal_store import get_proposals

router = APIRouter()


@router.get("/beliefs/{event_id}")
def get_belief(event_id: str, entity_id: str = Query(...)):
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
    history = get_belief_history(event_id, entity_id, limit=20)

    return [
        {
            "belief_id": b.belief_id,
            "probability": b.probability,
            "confidence": b.confidence,
            "as_of": b.as_of,
        }
        for b in history
    ]


@router.get("/beliefs/{event_id}/explain")
def explain_belief(event_id: str, entity_id: str = Query(...)):
    belief = get_latest_belief(event_id, entity_id)

    if belief is None:
        raise HTTPException(status_code=404, detail="Belief not found")

    proposals = get_proposals(event_id, entity_id)

    if not proposals:
        contributing_agents = []
        rationale = "No agent proposals available for this belief."
    else:
        contributing_agents = [
            {
                "agent_id": p.agent_id,
                "proposed_probability": p.proposed_probability,
            }
            for p in proposals
        ]
        rationale = " | ".join(p.rationale for p in proposals)

    return {
        "belief_id": belief.belief_id,
        "event_id": belief.event_id,
        "entity_id": entity_id,
        "probability": belief.probability,
        "confidence": belief.confidence,
        "contributing_agents": contributing_agents,
        "rationale": rationale,
    }
