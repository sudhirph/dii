from dataclasses import dataclass
from datetime import datetime


@dataclass
class DecisionSuggestion:
    """Lightweight dataclass for decision suggestions. No persistence, no methods."""
    entity_id: str
    event_id: str
    suggestion: str
    reason: str
    as_of: datetime

