# DII — Decision Intelligence Infrastructure (MVP)

## What this is
This repository contains the MVP for **Decision Intelligence Infrastructure (DII)**, starting with a **VC portfolio intelligence** use case.

The goal of this MVP is to help VC partners:
- Understand what is likely to happen across their portfolio
- See how beliefs about future outcomes change over time
- Understand *why* those beliefs changed
- Decide where intervention may matter before outcomes are obvious

This is a **decision support system**, not a prediction engine.

---

## What this MVP is NOT
This MVP is explicitly NOT:
- A deal sourcing tool
- A valuation or IRR model
- A trading or prediction market system
- A chatbot or AI copilot
- A healthcare or fintech product
- A real-time analytics system
- A production-scale platform
- A compliance-certified system (SOC2, HIPAA, etc.)

Anything outside the VC portfolio intelligence use case is out of scope for this MVP.

---

## Target users
- General Partners
- Portfolio Partners
- VC firm operators supporting portfolio decisions

---

## Core idea
Customer data is ingested once, converted into structured **signals**, and discarded.
Agents reason over signals to propose beliefs.
Beliefs are versioned, explainable, and auditable over time.
Decisions are logged against belief snapshots.
Outcomes close the loop and improve calibration.

---

## MVP success criteria
This MVP is successful if a VC partner can say:
> “This helped me understand what changed in my portfolio and where I should focus my time.”

Accuracy is secondary to clarity, explainability, and trust.



---

## Scope freeze (Day 1 decision)

### IN SCOPE
- One domain: VC portfolio decision intelligence
- One tenant (single VC firm)
- ~10–15 forecastable events
- Rule-based signal extraction
- Simple agent logic (no ML training)
- Probabilistic beliefs with explanations
- Manual outcome resolution

### OUT OF SCOPE
- Healthcare, fintech, or consumer use cases
- Deal sourcing or CRM
- Valuation or exit prediction
- Public market data
- Automated recommendations
- Chat-based UI
- Fine-tuning or custom ML models
- Multi-region infrastructure
- Compliance certifications
