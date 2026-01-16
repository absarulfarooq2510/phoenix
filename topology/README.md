# Topology Semantics — Phoenix

This directory contains the logical topology used by Phoenix to understand system structure and intent.

## Key Fields

### `role: "entry-point"`
Marks the logical starting point for discovery and system traversal.
Phoenix uses this node as the anchor from which downstream components are contextualized.

### `critical: true`
Indicates a business-critical component whose degradation has direct user, SLA, or revenue impact.

Phoenix uses this flag to:
- weight anomaly confidence more heavily
- lower escalation thresholds for critical paths
- classify incidents involving these components as higher severity

This flag does NOT trigger escalation on its own.
Correlation and confidence checks are still required.
