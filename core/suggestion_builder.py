from datetime import datetime
from typing import List

from core.alerts import AlertCandidate
from core.suggestions import DecisionSuggestion


def build_suggestions(alerts: List[AlertCandidate]) -> List[DecisionSuggestion]:
    """Build decision suggestions from alert candidates.
    
    Args:
        alerts: List of AlertCandidate objects
        
    Returns:
        Flat list of DecisionSuggestion objects (2-3 suggestions per alert)
    """
    suggestions = []
    
    for alert in alerts:
        # Generate 2-3 suggestions based on alert properties
        alert_suggestions = _generate_suggestions_for_alert(alert)
        suggestions.extend(alert_suggestions)
    
    return suggestions


def _generate_suggestions_for_alert(alert: AlertCandidate) -> List[DecisionSuggestion]:
    """Generate 2-3 suggestions for a single alert."""
    suggestions = []
    prob_pct = f"{alert.probability * 100:.1f}%"
    
    # Base suggestion based on change_type
    if alert.change_type == "significant_drop":
        suggestions.append(
            DecisionSuggestion(
                entity_id=alert.entity_id,
                event_id=alert.event_id,
                suggestion="Review recent signals and update risk assessment",
                reason=f"Alert: {alert.reason} - Probability dropped to {prob_pct}",
                as_of=alert.as_of,
            )
        )
        suggestions.append(
            DecisionSuggestion(
                entity_id=alert.entity_id,
                event_id=alert.event_id,
                suggestion="Consider reducing exposure or increasing monitoring frequency",
                reason=f"Alert: {alert.reason} - Significant probability decline detected",
                as_of=alert.as_of,
            )
        )
        if alert.probability < 0.3:
            suggestions.append(
                DecisionSuggestion(
                    entity_id=alert.entity_id,
                    event_id=alert.event_id,
                    suggestion="Escalate for immediate review and potential action",
                    reason=f"Alert: {alert.reason} - Probability below 30% threshold",
                    as_of=alert.as_of,
                )
            )
    
    elif alert.change_type == "significant_rise":
        suggestions.append(
            DecisionSuggestion(
                entity_id=alert.entity_id,
                event_id=alert.event_id,
                suggestion="Review positive signals and validate probability increase",
                reason=f"Alert: {alert.reason} - Probability increased to {prob_pct}",
                as_of=alert.as_of,
            )
        )
        suggestions.append(
            DecisionSuggestion(
                entity_id=alert.entity_id,
                event_id=alert.event_id,
                suggestion="Consider increasing allocation or follow-up analysis",
                reason=f"Alert: {alert.reason} - Significant probability improvement",
                as_of=alert.as_of,
            )
        )
        if alert.probability > 0.7:
            suggestions.append(
                DecisionSuggestion(
                    entity_id=alert.entity_id,
                    event_id=alert.event_id,
                    suggestion="High probability - prepare for potential event outcome",
                    reason=f"Alert: {alert.reason} - Probability above 70% threshold",
                    as_of=alert.as_of,
                )
            )
    
    elif alert.change_type == "initial":
        suggestions.append(
            DecisionSuggestion(
                entity_id=alert.entity_id,
                event_id=alert.event_id,
                suggestion="Establish baseline monitoring and set review schedule",
                reason=f"Alert: {alert.reason} - Initial belief established",
                as_of=alert.as_of,
            )
        )
        suggestions.append(
            DecisionSuggestion(
                entity_id=alert.entity_id,
                event_id=alert.event_id,
                suggestion="Gather additional signals to improve confidence",
                reason=f"Alert: {alert.reason} - New entity requires signal collection",
                as_of=alert.as_of,
            )
        )
        if alert.confidence == "low":
            suggestions.append(
                DecisionSuggestion(
                    entity_id=alert.entity_id,
                    event_id=alert.event_id,
                    suggestion="Prioritize signal collection to increase confidence level",
                    reason=f"Alert: {alert.reason} - Low confidence requires more data",
                    as_of=alert.as_of,
                )
            )
    
    # Ensure we return at least 2 suggestions
    if len(suggestions) < 2:
        suggestions.append(
            DecisionSuggestion(
                entity_id=alert.entity_id,
                event_id=alert.event_id,
                suggestion="Monitor entity and track belief evolution",
                reason=f"Alert: {alert.reason} - Standard monitoring recommended",
                as_of=alert.as_of,
            )
        )
    
    return suggestions

