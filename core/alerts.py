from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class AlertCandidate:
    """Lightweight dataclass for alert candidates. No persistence, no methods."""
    entity_id: str
    event_id: str
    probability: float
    delta: Optional[float]
    change_type: str
    confidence: str
    priority_rank: int
    reason: str
    as_of: datetime

