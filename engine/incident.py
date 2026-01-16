"""
Incident Escalation Engine for Phoenix

This module decides whether correlated deviations
justify raising a support incident.

It represents the final decision layer in Phoenix.
"""

import uuid
from datetime import datetime, timedelta


class IncidentManager:
    def __init__(self, topology, cooldown_seconds=300):
        """
        Initialize the incident manager.

        topology:
            Parsed topology with node metadata
            (used to identify critical components).

        cooldown_seconds:
            Minimum time between similar incidents
            to avoid repeated escalation.
        """
        self.topology = topology
        self.cooldown = timedelta(seconds=cooldown_seconds)
        self.last_incident_time = None

        # Precompute critical components for quick lookup
        self.critical_components = {
            node["id"]
            for node in topology["nodes"]
            if node.get("critical", False)
        }

    def evaluate(self, correlation_group):
        """
        Evaluate a correlated group of deviations and
        decide whether to raise an incident.

        Returns:
            Incident dictionary if escalation is justified,
            otherwise None.
        """

        now = datetime.utcnow()

        # Cooldown check to prevent alert storms
        if self.last_incident_time and now - self.last_incident_time < self.cooldown:
            return None

        components = {d["component"] for d in correlation_group}

        # Require multiple affected components
        if len(components) < 2:
            return None

        # Check deviation strength
        strong_deviations = [
            d for d in correlation_group
            if d["level"] == "strong"
        ]

        if not strong_deviations:
            return None

        # Check if any critical component is involved
        critical_involved = bool(
            components & self.critical_components
        )

        # Compute confidence score (simple, explainable)
        confidence = min(
            1.0,
            0.5
            + 0.2 * len(strong_deviations)
            + (0.2 if critical_involved else 0.0)
        )

        # Final safety check
        if confidence < 0.7:
            return None

        # Incident is justified
        self.last_incident_time = now

        return {
            "incident_id": f"INC-{uuid.uuid4().hex[:8]}",
            "timestamp": now.isoformat(),
            "severity": "high" if critical_involved else "medium",
            "confidence": round(confidence, 2),
            "affected_components": list(components),
            "critical_involved": critical_involved,
            "summary": "Correlated system degradation detected",
            "details": correlation_group
        }
