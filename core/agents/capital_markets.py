import uuid
from datetime import datetime
from typing import List

from core.agents.base import BaseAgent
from core.proposals import ForecastProposal
from core.signals import Signal


class CapitalMarketsAgent(BaseAgent):
    """Agent that generates forecasts for capital markets events based on financial signals."""
    
    agent_id: str = "capital_markets_agent_v1"
    supported_events: List[str] = ["NEXT_ROUND_RAISED"]
    required_signals: List[str] = ["runway_months", "burn_rate", "hiring_signal"]
    
    def generate_proposals(self, signals: List[Signal]) -> List[ForecastProposal]:
        """Generate forecast proposal based on financial signals."""
        # Extract signals by type
        signal_map = {signal.signal_type: signal for signal in signals}
        
        # Get entity_id from first signal (assuming all signals are for same entity)
        entity_id = signals[0].entity_id if signals else "unknown"
        
        # Start with base probability
        probability = 0.6
        
        # Apply adjustments based on signals
        adjustments = []
        
        # Check runway_months
        if "runway_months" in signal_map:
            runway_signal = signal_map["runway_months"]
            runway_value = runway_signal.value
            if isinstance(runway_value, (int, float)) and runway_value < 6:
                probability -= 0.15
                adjustments.append(f"runway below 6 months ({runway_value})")
        
        # Check burn_rate
        if "burn_rate" in signal_map:
            burn_signal = signal_map["burn_rate"]
            if burn_signal.value is True:
                probability -= 0.1
                adjustments.append("high burn rate detected")
        
        # Check hiring_signal
        if "hiring_signal" in signal_map:
            hiring_signal = signal_map["hiring_signal"]
            if hiring_signal.value is True:
                probability -= 0.05
                adjustments.append("active hiring detected")
        
        # Clamp probability between 0 and 1
        probability = max(0.0, min(1.0, probability))
        
        # Generate rationale
        if adjustments:
            rationale = f"Base probability 0.6 adjusted by: {', '.join(adjustments)}. Final probability: {probability:.2f}"
        else:
            rationale = f"Base probability 0.6 with no negative adjustments. Final probability: {probability:.2f}"
        
        # Create proposal
        proposal = ForecastProposal(
            proposal_id=str(uuid.uuid4()),
            agent_id=self.agent_id,
            event_id="NEXT_ROUND_RAISED",
            entity_id=entity_id,
            proposed_probability=probability,
            rationale=rationale,
            created_at=datetime.utcnow(),
        )
        
        return [proposal]

