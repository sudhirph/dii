from abc import ABC, abstractmethod
from typing import List

from core.proposals import ForecastProposal
from core.signals import Signal


class BaseAgent(ABC):
    """Abstract base class for forecast agents."""
    
    agent_id: str
    supported_events: List[str]
    required_signals: List[str]
    
    @abstractmethod
    def generate_proposals(self, signals: List[Signal]) -> List[ForecastProposal]:
        """Generate forecast proposals based on signals.
        
        Args:
            signals: List of Signal objects to process
            
        Returns:
            List of ForecastProposal objects
        """
        pass

