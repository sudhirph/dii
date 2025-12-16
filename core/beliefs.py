from datetime import datetime
from typing import Optional, Tuple

from pydantic import BaseModel, Field


class BeliefSnapshot(BaseModel):
    belief_id: str
    event_id: str
    entity_id: str
    probability: float = Field(ge=0, le=1)
    confidence: str  # low / medium / high
    confidence_interval: Optional[Tuple[float, float]] = None
    as_of: datetime
    previous_belief_id: Optional[str] = None

