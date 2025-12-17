from core.db import get_connection
from core.proposals import ForecastProposal


def insert_proposal(proposal: ForecastProposal):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO forecast_proposals (proposal_id, agent_id, event_id, entity_id, proposed_probability, rationale, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    proposal.proposal_id,
                    proposal.agent_id,
                    proposal.event_id,
                    proposal.entity_id,
                    proposal.proposed_probability,
                    proposal.rationale,
                    proposal.created_at,
                ),
            )
        conn.commit()
    finally:
        conn.close()


def get_proposals(event_id: str, entity_id: str):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT proposal_id, agent_id, event_id, entity_id, proposed_probability, rationale, created_at
                FROM forecast_proposals
                WHERE event_id = %s AND entity_id = %s
                ORDER BY created_at DESC
                """,
                (event_id, entity_id),
            )
            rows = cur.fetchall()
            return [
                ForecastProposal(
                    proposal_id=row[0],
                    agent_id=row[1],
                    event_id=row[2],
                    entity_id=row[3],
                    proposed_probability=row[4],
                    rationale=row[5],
                    created_at=row[6],
                )
                for row in rows
            ]
    finally:
        conn.close()

