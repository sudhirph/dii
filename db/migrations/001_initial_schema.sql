CREATE TABLE events (
    event_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    resolution_type TEXT NOT NULL,
    resolve_by TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE signals (
    signal_id TEXT PRIMARY KEY,
    entity_id TEXT NOT NULL,
    signal_type TEXT NOT NULL,
    value JSONB NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    source TEXT,
    confidence_hint FLOAT,
    created_at TIMESTAMP DEFAULT now()
);

CREATE INDEX idx_signals_entity_signal_type ON signals (entity_id, signal_type);

CREATE TABLE forecast_proposals (
    proposal_id TEXT PRIMARY KEY,
    agent_id TEXT NOT NULL,
    event_id TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    proposed_probability FLOAT NOT NULL,
    rationale TEXT,
    created_at TIMESTAMP DEFAULT now()
);

CREATE INDEX idx_forecast_proposals_event_entity ON forecast_proposals (event_id, entity_id);

CREATE TABLE belief_snapshots (
    belief_id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    probability FLOAT NOT NULL,
    confidence TEXT NOT NULL,
    confidence_interval JSONB,
    as_of TIMESTAMP NOT NULL,
    previous_belief_id TEXT NULL,
    created_at TIMESTAMP DEFAULT now()
);

CREATE INDEX idx_belief_snapshots_event_entity_as_of ON belief_snapshots (event_id, entity_id, as_of);

