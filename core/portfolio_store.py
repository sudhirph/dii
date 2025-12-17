from typing import List, Optional

from core.beliefs import BeliefSnapshot
from core.db import get_connection


def get_entities_with_beliefs(event_id: str) -> List[str]:
    """Get all distinct entity_ids that have beliefs for a given event.
    
    Args:
        event_id: The event identifier
        
    Returns:
        List of distinct entity_id strings
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT DISTINCT entity_id
                FROM belief_snapshots
                WHERE event_id = %s
                ORDER BY entity_id
                """,
                (event_id,),
            )
            rows = cur.fetchall()
            return [row[0] for row in rows]
    finally:
        conn.close()


def get_previous_belief(event_id: str, entity_id: str, current_belief_id: str) -> Optional[BeliefSnapshot]:
    """Get the previous belief snapshot before the current one.
    
    Args:
        event_id: The event identifier
        entity_id: The entity identifier
        current_belief_id: The belief_id of the current belief
        
    Returns:
        The previous BeliefSnapshot or None if not found
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Single query using subquery to get previous belief
            cur.execute(
                """
                SELECT bs.belief_id, bs.event_id, bs.entity_id, bs.probability, bs.confidence, bs.confidence_interval, bs.as_of, bs.previous_belief_id
                FROM belief_snapshots bs
                WHERE bs.event_id = %s 
                  AND bs.entity_id = %s 
                  AND bs.as_of < (
                      SELECT as_of 
                      FROM belief_snapshots 
                      WHERE belief_id = %s
                  )
                ORDER BY bs.as_of DESC
                LIMIT 1
                """,
                (event_id, entity_id, current_belief_id),
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

