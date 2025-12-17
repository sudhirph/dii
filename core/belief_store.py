import json
from typing import Optional

from core.beliefs import BeliefSnapshot
from core.db import get_connection


def get_latest_belief(event_id: str, entity_id: str) -> Optional[BeliefSnapshot]:
    """Get the most recent belief snapshot for a given event and entity.
    
    Args:
        event_id: The event identifier
        entity_id: The entity identifier
        
    Returns:
        The most recent BeliefSnapshot or None if not found
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT belief_id, event_id, entity_id, probability, confidence, confidence_interval, as_of, previous_belief_id
                FROM belief_snapshots
                WHERE event_id = %s AND entity_id = %s
                ORDER BY as_of DESC
                LIMIT 1
                """,
                (event_id, entity_id),
            )
            row = cur.fetchone()
            if row is None:
                return None
            
            # Parse confidence_interval from JSONB if present
            confidence_interval = None
            if row[5] is not None:
                confidence_interval = tuple(row[5]) if isinstance(row[5], list) else row[5]
            
            return BeliefSnapshot(
                belief_id=row[0],
                event_id=row[1],
                entity_id=row[2],
                probability=row[3],
                confidence=row[4],
                confidence_interval=confidence_interval,
                as_of=row[6],
                previous_belief_id=row[7],
            )
    finally:
        conn.close()


def get_belief_history(event_id: str, entity_id: str, limit: int = 20):
    """Get belief history for a given event and entity.
    
    Args:
        event_id: The event identifier
        entity_id: The entity identifier
        limit: Maximum number of records to return (default: 20)
        
    Returns:
        List of dictionaries with: belief_id, probability, confidence, as_of
        Ordered by as_of ascending (oldest first)
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT belief_id, probability, confidence, as_of
                FROM belief_snapshots
                WHERE event_id = %s AND entity_id = %s
                ORDER BY as_of ASC
                LIMIT %s
                """,
                (event_id, entity_id, limit),
            )
            rows = cur.fetchall()
            return [
                {
                    "belief_id": row[0],
                    "probability": row[1],
                    "confidence": row[2],
                    "as_of": row[3],
                }
                for row in rows
            ]
    finally:
        conn.close()


def insert_belief_snapshot(belief: BeliefSnapshot):
    """Insert a new belief snapshot. Beliefs are immutable - this always creates a new record.
    
    Args:
        belief: The BeliefSnapshot to insert
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Convert confidence_interval tuple to JSONB if present
            confidence_interval_json = None
            if belief.confidence_interval is not None:
                confidence_interval_json = json.dumps(list(belief.confidence_interval))
            
            cur.execute(
                """
                INSERT INTO belief_snapshots (belief_id, event_id, entity_id, probability, confidence, confidence_interval, as_of, previous_belief_id)
                VALUES (%s, %s, %s, %s, %s, %s::jsonb, %s, %s)
                """,
                (
                    belief.belief_id,
                    belief.event_id,
                    belief.entity_id,
                    belief.probability,
                    belief.confidence,
                    confidence_interval_json,
                    belief.as_of,
                    belief.previous_belief_id,
                ),
            )
        conn.commit()
    finally:
        conn.close()

