# Phoenix
### Topology-First System Intelligence for Autonomous Incident Escalation

---

## Why Phoenix exists

### The real problem Phoenix is solving

Large enterprises increasingly build **temporary or rapidly evolving networks**:

- Global conferences and exhibitions  
- Large sporting events (Olympics, Commonwealth Games)  
- Pop-up data centers and regional expansions  
- Major migrations and re-architectures  

In these scenarios, networks are often built **from scratch under strict timelines**.

Yet the way enterprises operationalize these networks has not evolved at the same pace.

---

### How this is done today

Once a network topology is designed, teams must still:

- Manually onboard each router, switch, and application into monitoring systems  
- Upload CSV files or enter device details one by one  
- Configure discovery, metrics, and thresholds per device  
- Rely on humans to interpret dashboards and decide when to raise incidents  

This approach is **device-centric** and assumes:
- Static architectures  
- Ample time for configuration  
- Humans as the primary correlation engine  

These assumptions break down during large-scale or event-driven deployments.

---

### The core failure (root cause, not symptoms)

> **Operational tools understand devices, but humans understand topology.**

Network and platform teams reason in terms of:
- traffic paths  
- upstream and downstream dependencies  
- critical choke points  
- blast radius of failures  

Monitoring systems, however, see only:
- isolated devices  
- isolated metrics  
- isolated alerts  

As a result, humans are forced to:
- reconstruct topology mentally  
- correlate signals across layers  
- decide when degradation is “incident-worthy”  

Late incident detection is not the problem.  
**Manual operationalization is.**

---

### Why this matters most during large events

During high-stakes deployments:

- Onboarding hundreds of devices can take weeks  
- Monitoring coverage is often incomplete at go-live  
- Alert noise is high, insight is low  
- Incidents are raised **after user impact**, not before  

Teams do not lack data.  
They lack **system-level understanding**.

---

### What Phoenix changes

Phoenix starts **one step earlier** than traditional monitoring tools.

Instead of asking teams to explain their systems device by device, Phoenix asks:

**“If the topology already exists to build the network, why can’t the system learn from it directly?”**

Phoenix introduces a **topology-first approach** where:

- Teams provide the logical architecture of the system  
- Devices and services are discovered and contextualized automatically  
- Relationships are established before metrics are interpreted  
- System behavior is learned holistically, not per device  

This enables faster operational readiness and reduces dependency on manual configuration.

---

### Phoenix’s role (clear positioning)

Phoenix does **not** replace:
- device provisioning tools  
- controller-based discovery (PnP)  
- existing monitoring or observability platforms  

Instead, Phoenix sits **above them**, providing:

> **Topology-aware system intelligence that accelerates onboarding and enables autonomous, high-confidence incident escalation.**

---

## How Phoenix works (Conceptual)

Phoenix is designed as a **topology-first system**, not a device-first monitoring tool.  
Its workflow mirrors how network and platform teams reason about systems in the real world.

---

### 1. Topology-first ingestion

Phoenix begins with a **logical topology** that represents how the system is designed to function.

Instead of onboarding individual devices one by one, teams provide a topology that describes:
- network components (routers, switches, gateways)
- application services
- dependencies and traffic paths between them

This topology acts as the **operational intent** of the system.

> In Phoenix, topology is not configuration — it is context.

---

### 2. Discovery starting point and system expansion

Using the provided topology, Phoenix identifies a **logical starting point** for discovery — typically an edge, gateway, or controller-like node.

From this anchor, Phoenix:
- expands outward across the topology  
- contextualizes downstream components  
- establishes upstream/downstream relationships  
- prepares the system graph for learning and correlation  

Discovery is guided by **structure**, not static device lists.

---

### 3. Learning system behavior (not thresholds)

Once components are contextualized, Phoenix observes telemetry across the system.

Rather than relying on predefined thresholds:
- Phoenix learns normal behavior over time  
- baselines are established per component and per relationship  
- deviations are evaluated in context, not isolation  

This allows Phoenix to distinguish between:
- expected fluctuations  
- localized noise  
- system-level degradation  

Learning happens continuously and quietly in the background.

---

### 4. Topology-aware correlation and escalation

When anomalies occur, Phoenix does not treat signals independently.

Instead, it asks:
- Do multiple signals align along the topology?
- Is there a plausible propagation path?
- Does the degradation affect critical dependencies?

Only when confidence is high does Phoenix **autonomously raise a support incident**, attaching:
- affected components  
- degradation timeline  
- suspected propagation path  
- confidence score  

The goal is not more alerts — it is **earlier, more trustworthy escalation**.

---

### 5. Scope and evolution

Phoenix is intentionally built in phases.

**Phoenix v1**
- Predefined sample topology  
- Topology-driven discovery simulation  
- Automatic contextualization of components  
- Cross-layer behavior learning (network + application)  
- Autonomous incident detection and escalation (detect + raise)  

**Future iterations**
- Visual topology diagram ingestion  
- Integration with controller-based discovery (PnP)  
- Vendor and API-based device discovery  
- Intent-aware traffic modeling  
- Integration with real ticketing and ITSM systems  

Phoenix prioritizes correctness, trust, and explainability before scale.

---

## Design documentation

Detailed design decisions — including topology schemas, discovery assumptions, learning lifecycle, correlation logic, and trade-offs — are documented in:

📄 `docs/system-design.pdf`

---

## Why this project matters

Phoenix is not a chatbot or UI-centric AI demo.

It is a **system-thinking exercise** focused on:
- enterprise constraints  
- topology-aware intelligence  
- false-positive avoidance  
- explainable autonomy  
- real operational pain points  

This project explores how AI can be embedded **deep in backend systems**, where its value is measured by **reduced human effort and earlier incident readiness**, not by conversational interfaces.

---

## Status

🚧 **Work in progress**

Phoenix is being built incrementally, starting with a predefined sample architecture and simulated telemetry to demonstrate end-to-end learning and autonomous escalation.
