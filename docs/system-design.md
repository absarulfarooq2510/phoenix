# Phoenix — System Design Document

---

## 1. Executive Summary

### Purpose of this document

This document describes the design of **Phoenix**, a topology-first system that accelerates operational readiness and enables autonomous incident escalation in enterprise networks.

It explains:
- the problem Phoenix is solving
- the design principles guiding the system
- how topology, discovery, learning, and escalation work together
- the scope boundaries of v1 and planned evolution

This document intentionally focuses on **design reasoning and trade-offs**, not tool-specific implementation.

---

## 2. Problem Context & Motivation

### 2.1 Operational reality in large-scale deployments

Modern enterprises increasingly operate:
- event-driven networks (sports events, conferences)
- temporary or rapidly evolving infrastructures
- systems built under strict timelines and public visibility

During such deployments:
- network architectures are designed quickly
- devices and services are provisioned in parallel
- operational readiness often lags deployment

---

### 2.2 Why existing approaches fail

Current operational tooling requires:
- device-by-device onboarding
- CSV uploads or manual configuration
- predefined metrics and thresholds
- human-driven interpretation of dashboards

These approaches are:
- device-centric
- slow to operationalize
- disconnected from architectural intent

Humans are forced to act as the correlation and escalation engine.

---

### 2.3 Design goal

> Reduce human dependency in onboarding, correlation, and incident initiation by allowing the system to reason from topology and learn behavior autonomously.

---

## 3. Design Principles

Phoenix is guided by the following principles:

1. **Topology before telemetry**  
   Structure must exist before signals can be interpreted.

2. **Learning before alerting**  
   Systems must learn normal behavior before escalation.

3. **Correlation before escalation**  
   Single alerts are insufficient; system-level patterns matter.

4. **Explainability over aggressiveness**  
   False positives are costlier than delayed escalation.

5. **Augmentation, not replacement**  
   Phoenix complements existing controllers and monitoring tools.

---

## 4. System Overview (Logical Architecture)

### 4.1 High-level system flow

Topology Input
↓
Discovery & Contextualization
↓
Telemetry Ingestion
↓
Baseline Learning
↓
Deviation Detection
↓
Topology-aware Correlation
↓
Confidence Evaluation
↓
Incident Generation

---

### 4.2 System boundary

**Inside Phoenix**
- topology understanding
- relationship modeling
- behavior learning
- incident decisioning

**Outside Phoenix**
- device provisioning
- controller-based lifecycle management
- existing monitoring systems
- human remediation workflows

---

## 5. Topology Ingestion Model

### 5.1 What topology represents

Topology in Phoenix represents **operational intent**, not configuration.

It captures:
- components (network devices, services)
- relationships (dependencies, traffic paths)
- hierarchy (entry points, aggregation layers)

---

### 5.2 Why topology is the starting point

- mirrors how humans reason about systems
- enables blast-radius awareness
- guides discovery and correlation
- reduces manual configuration overhead

---

### 5.3 V1 topology assumptions

- predefined, structured topology
- provided as static input
- no visual diagram parsing in v1

---

## 6. Discovery Strategy & Starting Point Selection

### 6.1 Why discovery needs an anchor

Discovery must start from a **known, stable entry point** to:
- avoid ambiguity
- establish traversal order
- build consistent relationships

---

### 6.2 How Phoenix selects the starting point (conceptual)

- derived from topology (edge, gateway, or controller-like node)
- or manually specified by the user
- used as the root for system expansion

---

### 6.3 V1 constraints

- discovery is simulated or mocked
- focus is on contextualization, not protocol accuracy

---

## 7. Telemetry Model & Data Contracts

### 7.1 Telemetry philosophy

Phoenix treats telemetry as **signals**, not alerts.

Signals are:
- continuous
- noisy
- meaningless without context

---

### 7.2 Telemetry event schema (conceptual)

Each telemetry signal includes:
- timestamp
- component identifier
- metric type
- value
- contextual tags

Uniform schemas enable cross-layer learning and correlation.

---

## 8. Learning Lifecycle

### 8.1 Cold start phase

- observation-only mode
- no escalation
- baseline formation

---

### 8.2 Baseline stabilization

- normal ranges learned
- variance and seasonality understood
- relationship behavior established

---

### 8.3 Deviation detection

- statistically meaningful deviations
- context-aware evaluation
- no static thresholds

---

## 9. Correlation & Confidence Evaluation

### 9.1 Why correlation matters

Single-signal anomalies are unreliable.

Phoenix correlates:
- multiple signals
- across components
- along topology paths

---

### 9.2 Confidence scoring

Confidence is based on:
- signal alignment
- topology consistency
- temporal persistence

Escalation requires **high confidence by design**.

---

## 10. Incident Generation & Escalation

### 10.1 When an incident is created

An incident is generated only when:
- degradation is system-level
- confidence threshold is met
- cooldown conditions allow escalation

---

### 10.2 Incident contents

Each incident includes:
- affected components
- degradation timeline
- suspected propagation path
- confidence score
- explanatory context

Phoenix raises incidents; humans decide remediation.

---

## 11. Scope Definition

### 11.1 Phoenix v1 (this project)

- predefined topology
- simulated discovery
- real learning logic
- topology-aware correlation
- autonomous incident creation

---

### 11.2 Explicit non-goals for v1

- auto-remediation
- guaranteed root cause
- real device integrations
- production-scale optimization

---

## 12. Future Evolution

Planned extensions include:
- visual topology ingestion
- controller-based discovery integration (PnP)
- vendor and API-based device discovery
- intent-aware traffic modeling
- ITSM / ticketing integrations

---

## 13. Key Trade-offs & Risks

- conservative escalation vs speed
- simulated discovery vs realism
- learning time vs readiness
- explainability vs complexity

Each trade-off is intentional and aligned with Phoenix’s goals.

---

## 14. Conclusion

Phoenix demonstrates how **topology-first thinking**, combined with **responsible AI**, can reduce operational friction and improve incident readiness in complex enterprise systems.

The project prioritizes:
- correctness over completeness
- trust over automation
- system intelligence over dashboards
