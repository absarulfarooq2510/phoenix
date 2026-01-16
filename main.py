"""
Phoenix — End-to-End Runner

This script wires together all Phoenix components:
- telemetry ingestion
- baseline learning
- deviation detection
- topology-aware correlation
- incident escalation

Running this file simulates Phoenix observing a system
and autonomously raising incidents when confidence is high.
"""

import time
import json

from telemetry.signal_generator import generate_signal
from engine.baseline import BaselineLearner
from engine.deviation import DeviationDetector
from engine.correlator import Correlator
from engine.incident import IncidentManager

# -------------------------------------------------------------------
# Load topology
# -------------------------------------------------------------------

with open("topology/sample-topology.json") as f:
    topology = json.load(f)

# -------------------------------------------------------------------
# Initialize Phoenix components
# -------------------------------------------------------------------

baseline_learner = BaselineLearner(min_samples=30)
deviation_detector = DeviationDetector(baseline_learner)
correlator = Correlator(topology)
incident_manager = IncidentManager(topology)

# Components and metrics (same as telemetry generator)
COMPONENTS = [
    "router-edge",
    "switch-aggregation",
    "api-gateway",
    "order-service",
    "payment-service"
]

METRICS = {
    "router-edge": ["latency_ms", "packet_drop_rate"],
    "switch-aggregation": ["latency_ms"],
    "api-gateway": ["p95_latency_ms", "error_rate"],
    "order-service": ["p95_latency_ms", "error_rate"],
    "payment-service": ["p95_latency_ms", "error_rate"]
}

print("\nPhoenix started — learning system behavior...\n")

# -------------------------------------------------------------------
# Main event loop
# -------------------------------------------------------------------

while True:
    for component in COMPONENTS:
        for metric in METRICS[component]:

            # 1. Generate telemetry signal
            signal = generate_signal(component, metric)
            value = signal["value"]

            # 2. Update baseline learning
            baseline_learner.update(component, metric, value)

            # 3. Evaluate deviation (if baseline is ready)
            deviation = deviation_detector.evaluate(component, metric, value)

            if deviation:
                # 4. Record deviation for correlation
                correlator.record_deviation(deviation)

                # 5. Attempt correlation
                correlation_groups = correlator.correlate()

                # 6. Evaluate each correlation group for escalation
                for group in correlation_groups:
                    incident = incident_manager.evaluate(group)

                    if incident:
                        print("\n🔥 INCIDENT RAISED 🔥")
                        print(json.dumps(incident, indent=2))
                        print("\n")

    # Sleep to simulate real-time signal flow
    time.sleep(2)
