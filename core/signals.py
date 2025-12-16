from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class Signal(BaseModel):
    signal_id: str
    entity_id: str
    signal_type: str
    value: Any
    timestamp: datetime
    source: str
    confidence_hint: Optional[float] = Field(None, ge=0, le=1)

