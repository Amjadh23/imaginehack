# Graph Report - ImagineHack  (2026-06-20)

## Corpus Check
- 17 files · ~16,634 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 167 nodes · 151 edges · 16 communities
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]

## God Nodes (most connected - your core abstractions)
1. `11 — UI/UX Specification` - 12 edges
2. `04 — SDD: Module 1, Detection & Insight` - 11 edges
3. `05 — SDD: Module 2, Next Best Action` - 10 edges
4. `06 — SDD: Module 3, Guardrailed Self-Healing` - 10 edges
5. `13 — Safety, Governance & Audit` - 10 edges
6. `02 — High-Level Architecture` - 9 edges
7. `03 — Unified Data Model` - 9 edges
8. `10 — API Contracts (merged)` - 9 edges
9. `01 — Project Context` - 8 edges
10. `7. Kept old-spec objects` - 8 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (16 total, 0 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.12
Nodes (16): 03 — Unified Data Model, 1. Canonical entity graph, 2. Workload, 3. TelemetrySnapshot (Module 1 input), 4. Issue (Module 1 output / Module 2 input), 5. Recommendation (Module 2 output / Module 3 input), 6. Remediation Result + Report, 7. Kept old-spec objects (+8 more)

### Community 1 - "Community 1"
Cohesion: 0.13
Nodes (14): 10. Acceptance criteria, 11 — UI/UX Specification, 1. Dashboard / Heatmap landing — BOTH views (decision), 2. Issues List (NEW page), 3. Issue / Recommendation Detail (NEW page), 4. Workload Detail tabs (kept from prototype), 5. Self-Healing workflow page, 6. Approval Queue (kept) (+6 more)

### Community 2 - "Community 2"
Cohesion: 0.15
Nodes (12): 07 — SDD: Scoring & Alerts (kept from old spec), A1. Weighted Priority Score, A2. Rules, A3. Component scores (existing formulas, kept), A4. DimensionScores (matrix heatmap), B1. Conditions, B2. Severity from Priority_Score, B3. Delivery & lifecycle (+4 more)

### Community 3 - "Community 3"
Cohesion: 0.17
Nodes (11): 04 — SDD: Module 1, Detection & Insight, 10. Acceptance criteria, 1. Purpose, 2. Flow, 3. Input / Output, 4. Isolation Forest (anomaly), 5. Rule-based issue classification, 6. Severity logic (+3 more)

### Community 4 - "Community 4"
Cohesion: 0.18
Nodes (10): 05 — SDD: Module 2, Next Best Action, 1. Purpose, 2. Flow, 3. Approach, 4. Recommendation rules, 5. Risk level, 6. Execution mode, 7. Optimization Impact Forecast (key new feature) (+2 more)

### Community 5 - "Community 5"
Cohesion: 0.18
Nodes (10): 06 — SDD: Module 3, Guardrailed Self-Healing, 1. Purpose, 2. Execution sequence (kept from old spec), 3. Execution paths, 4. Safety rules (authoritative — see `13` for full detail), 5. Runbooks + rollback (kept, detailed), 6. Simulated MCP connectors, 7. Approval Queue + escalation timers (kept from old spec) (+2 more)

### Community 6 - "Community 6"
Cohesion: 0.18
Nodes (10): 13 — Safety, Governance & Audit, 1. Decision question, 2. Auto-fix allowed (ALL must hold), 3. Approval required (any), 4. Human escalation required (any), 5. Prohibited auto actions (never), 6. Audit log (every meaningful event), 7. Remediation report (after auto-fix / approved / escalation) (+2 more)

### Community 7 - "Community 7"
Cohesion: 0.20
Nodes (9): 02 — High-Level Architecture, 1. Core flow, 2. Layers, 3. System diagram, 4. Module-to-module data contracts, 5. ML placement (full stack), 6. Both heatmaps (decision: Both), 7. Architectural decisions (+1 more)

### Community 8 - "Community 8"
Cohesion: 0.20
Nodes (9): 10 — API Contracts (merged), 1. Telemetry & workloads, 2. Detection / Issues, 3. Recommendations / Forecast, 4. Remediation / Approvals, 5. Scoring / Alerts / Audit, 6. Dashboard, 7. Mock controller (+1 more)

### Community 9 - "Community 9"
Cohesion: 0.22
Nodes (8): 01 — Project Context, Hackathon, MVP honesty, Problem, Product name, Solution, Track relevance, Winning angle

### Community 10 - "Community 10"
Cohesion: 0.22
Nodes (8): 08 — SDD: AI Downtime Prediction (KEPT), 1. Purpose, 2. Inputs, 3. Outputs (`DowntimePrediction`), 4. Relationship to the other ML, 5. UI, 6. Fallback, 7. Acceptance criteria

### Community 11 - "Community 11"
Cohesion: 0.22
Nodes (8): 09 — SDD: ML, Explainability & Forecasting (full stack), 1. Isolation Forest, 2. SHAP / SHAP-style, 3. XGBoost forecasting, 4. Synthetic training data, 5. Optimization Impact Forecast, 6. Fallbacks (must keep output schema), 7. Acceptance criteria

### Community 12 - "Community 12"
Cohesion: 0.22
Nodes (8): 12 — Mock Data & Demo Scenarios, 1. Generator responsibilities, 2. Synthetic workloads (≥8), 3. Demo scenarios (trigger → expected behavior), 4. Stream + reset, 5. Deliverables (AI/mock subteam), 6. Suggested live demo order, 7. Backup plan

### Community 13 - "Community 13"
Cohesion: 0.25
Nodes (7): 14 — Implementation Plan (phased), Engineering risks, P0 — Demo-critical (must-have for the pitch), P1 — Credibility & governance, P2 — Depth (stretch; kept-from-old-spec), Suggested file structure, Team split

### Community 14 - "Community 14"
Cohesion: 0.25
Nodes (7): 15 — Traceability Matrix, A. New HILTI docs → merged, B. Old CloudGuard requirements → merged, C. Decisions log, D. Added (new vs prototype) — the build gaps, E. Consciously NOT dropped (preserved from old/prototype), F. Source folders status

### Community 15 - "Community 15"
Cohesion: 0.40
Nodes (4): Engineering principle, Locked reconciliation decisions (2026-06-20), Reading order, Reconciled SDD — CloudGuard GreenOps / HILTI Cloud Intelligence

## Knowledge Gaps
- **132 isolated node(s):** `Locked reconciliation decisions (2026-06-20)`, `Reading order`, `Engineering principle`, `Hackathon`, `Problem` (+127 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `Locked reconciliation decisions (2026-06-20)`, `Reading order`, `Engineering principle` to the rest of the system?**
  _132 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.11764705882352941 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._