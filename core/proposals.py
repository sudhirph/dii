from datetime import datetime

from pydantic import BaseModel, Field


class ForecastProposal(BaseModel):
    proposal_id: str
    agent_id: str
    event_id: str
    entity_id: str
    proposed_probability: float = Field(ge=0, le=1)
    rationale: str
    created_at: datetime

