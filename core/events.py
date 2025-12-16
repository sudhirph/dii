from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Event(BaseModel):
    event_id: str
    name: str
    description: str
    resolution_type: str  # e.g. binary, numeric
    resolve_by: Optional[datetime] = None
