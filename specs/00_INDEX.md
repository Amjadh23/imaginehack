# Reconciled SDD — Clover

This folder is the **single source of truth** for the MVP. It merges the two earlier,
conflicting doc sets:

- `md_file_old/` — the original formal spec (the prototype was built from this)
- `hilti_cloud_intelligence_docs/` — newer 3-module + ML re-framing

Where they disagreed, this folder encodes the resolved decisions. The two old folders
are now **reference/archive only** — build against this one.

---

## Locked reconciliation decisions (2026-06-20)

| Conflict | Decision |
|---|---|
| **Domain model** | **Unified** — one canonical entity carrying `telemetry → issue → recommendation → remediation` *and* keeping resource findings, weighted scores, runbooks, alerts. |
| **Heatmap** | **Both** — composite per-workload score grid as the landing, with a toggle into a workload×dimension matrix (Security / Energy / Carbon / Cost / Performance / Monitoring). |
| **AI/ML stack** | **Full new ML stack** — Isolation Forest (anomaly) + XGBoost (cost/energy/carbon forecast) + SHAP (explainability) + LLM (wording only). Safety decisions are rule-based, never the LLM. |
| **Kept from old spec** | 90-day uptime bar · weighted Priority Score · full alert system (suppression/retry/SLA) · detailed runbooks + rollback/verification. |
| **AI Downtime Prediction** | **Kept** — full ML stack *plus* the prototype's downtime panel (probability, time-to-failure, 12h risk timeline, preemptive action). |

---

## Reading order

| File | Purpose |
|---|---|
| `01_PROJECT_CONTEXT.md` | Track, problem, solution, winning angle |
| `02_ARCHITECTURE.md` | Unified architecture, module flow, ML placement, both heatmaps |
| `03_DATA_MODEL.md` | The unified entity + all sub-object schemas and enums |
| `04_DETECTION_AND_INSIGHT_SDD.md` | Module 1 — Isolation Forest + rules + SHAP + LLM |
| `05_NEXT_BEST_ACTION_SDD.md` | Module 2 — rule-based NBA + XGBoost + Optimization Impact Forecast |
| `06_GUARDRAILED_SELF_HEALING_SDD.md` | Module 3 — safety rules + runbooks + rollback + MCP + report |
| `07_SCORING_AND_ALERTS_SDD.md` | Weighted Priority Score (6 factors) + Alert system |
| `08_DOWNTIME_PREDICTION_SDD.md` | AI Downtime Prediction (kept feature) |
| `09_ML_AND_FORECASTING_SDD.md` | Models, features, training data, fallbacks |
| `10_API_CONTRACTS.md` | Merged REST + WebSocket endpoints |
| `11_UI_UX_SPECIFICATION.md` | All pages and components |
| `12_MOCK_DATA_AND_DEMO_SCENARIOS.md` | Generator, scenarios, acceptance |
| `13_SAFETY_GOVERNANCE_AUDIT.md` | Safety model, audit log, governance UI |
| `14_IMPLEMENTATION_PLAN.md` | Phased build plan (P0/P1/P2) |
| `15_TRACEABILITY_MATRIX.md` | Old reqs + new docs → merged; kept/dropped log |

---

## Engineering principle

```text
Detect clearly.   (Isolation Forest + SHAP + rules)
Recommend safely. (rule-based NBA + XGBoost forecast)
Fix responsibly.  (guardrailed self-healing, human-in-the-loop)
Report transparently. (remediation reports + audit log)
```

Do not overbuild. P0 is the demo. P1/P2 are credibility depth — treat P2 as stretch.
