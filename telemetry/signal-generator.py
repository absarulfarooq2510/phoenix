import time
import random
from datetime import datetime

# -------------------------------------------------------------------
# Telemetry Signal Generator for Phoenix
#
# This module simulates live telemetry emitted by network devices
# and application services in an enterprise system.
#
# The goal is NOT to simulate real packets or infrastructure,
# but to generate realistic health signals that Phoenix can:
#   - observe
#   - learn baseline behavior from
#   - correlate across topology
#   - use for autonomous incident escalation
# -------------------------------------------------------------------

# List of components present in the sample topology.
# These identifiers directly map to node IDs defined in
# topology/sample-topology.json.
COMPONENTS = [
    "router-edge",
    "switch-aggregation",
    "api-gateway",
    "order-service",
    "payment-service"
]

# Metrics emitted by each component.
# The choice of metrics is intentional:
# - Focus on service health and network quality
# - Avoid low-level host metrics (CPU, memory)
# - Keep signal-to-noise ratio high
METRICS = {
    "router-edge": ["latency_ms", "packet_drop_rate"],
    "switch-aggregation": ["latency_ms"],
    "api-gateway": ["p95_latency_ms", "error_rate"],
    "order-service": ["p95_latency_ms", "error_rate"],
    "payment-service": ["p95_latency_ms", "error_rate"]
}

def generate_signal(component, metric):
    """
    Generate a single telemetry signal for a given component and metric.

    This function represents the raw signal emission layer.
    It does NOT perform:
    - anomaly detection
    - threshold checks
    - correlation

    Those responsibilities belong to Phoenix's learning
    and decisioning layers.
    """

    # Baseline value ranges for each metric.
    # These ranges represent "normal" system behavior.
    #
    # Deviations from these ranges will later be used
    # by Phoenix to learn baselines and detect anomalies.
    base = {
        "latency_ms": random.uniform(10, 30),
        "p95_latency_ms": random.uniform(50, 120),
        "packet_drop_rate": random.uniform(0, 0.2),
        "error_rate": random.uniform(0, 0.01)
    }

    # Telemetry event structure.
    # This uniform schema allows Phoenix to treat
    # network and application signals consistently.
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "component": component,
        "metric": metric,
        "value": round(base[metric], 3)
    }

def run():
    """
    Main loop that continuously emits telemetry signals.

    In a real system:
    - Signals would arrive asynchronously
    - Data would be streamed via message queues or agents

    For Phoenix v1:
    - We emit signals synchronously
    - Output is printed to stdout for visibility and debugging
    """

    while True:
        # Iterate over all components in the topology
        for component in COMPONENTS:

            # Emit each metric relevant to the component
            for metric in METRICS[component]:
                signal = generate_signal(component, metric)

                # In v1, signals are printed.
                # In later iterations, this would be:
                # - pushed to a stream
                # - ingested by a learning engine
                print(signal)

        # Sleep to simulate periodic telemetry emission.
        # This interval represents the "heartbeat" of the system.
        time.sleep(2)

# Entry point for running the telemetry generator standalone.
# This allows Phoenix components to be developed and tested independently.
if __name__ == "__main__":
    run()
