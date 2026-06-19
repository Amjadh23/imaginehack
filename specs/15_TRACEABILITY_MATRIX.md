# 15 — Traceability Matrix

Maps the two source doc sets onto this merged spec, and logs what was kept, added, or dropped.

## A. New HILTI docs → merged
| New doc | Lands in |
|---|---|
| 00_README, 01_PROJECT_CONTEXT | 01 |
| 02_HIGH_LEVEL_ARCHITECTURE | 02 |
| 03_DATA_CONTRACTS | 03 (telemetry/issue/recommendation/remediation) |
| 04_MOCK_DATA_SPECIFICATION | 12 |
| 05_DETECTION_AND_INSIGHT_SDD | 04 |
| 06_NEXT_BEST_ACTION_SDD | 05 |
| 07_GUARDRAILED_SELF_HEALING_SDD | 06, 13 |
| 08_ML_AND_FORECASTING_SDD | 09 |
| 09_API_CONTRACTS | 10 |
| 10_UI_UX_SPECIFICATION | 11 |
| 11_DEMO_SCENARIOS_AND_ACCEPTANCE | 12 |
| 12_SAFETY_GOVERNANCE_AUDIT | 13 |
| 13_IMPLEMENTATION_PLAN | 14 |

## B. Legacy (original-spec) requirements → merged
| Old Req | Merged location | Note |
|---|---|---|
| 1 Workflow mapping | 03 (`construction_workflow`, criticality) | kept |
| 2 Resource monitoring | 03 telemetry, 10 ingest | kept (workload terms) |
| 3 Security detection/score | 04, 07A3 | kept (deduction formula) |
| 4 GreenOps efficiency | 05, 07A3 | kept |
| 5 AI diagnosis/recommendation | 04, 05 | LLM-wording + rule NBA |
| 6 Self-healing engine | 06 | kept, detailed (runbooks/rollback) |
| 7 Alert system | 07B | **kept** |
| 8 Dashboard | 11 | both heatmaps + tabs |
| 9 Demo scenarios | 12 | merged scenario set |
| 10 MCP execution | 03 §8, 06 | kept |
| 11 Scoring/prioritization | 07A | **kept** (weighted) |
| 12 Data simulation | 12 | kept |
| 13 Downtime prediction | 08 | **kept** |
| 14 Post-incident reports | 03 §6, 11 §7, 13 §7 | kept |
| 15 Approval queue | 06 §7, 11 §6 | kept |

## C. Decisions log
| # | Conflict | Decision |
|---|---|---|
| 1 | Domain model | **Unified** (workload carries pipeline + findings/scores/runbooks/alerts) |
| 2 | Heatmap | **Both** (composite grid + dimension matrix toggle) |
| 3 | AI/ML stack | **Full new ML** (Isolation Forest + XGBoost + SHAP + LLM-wording) |
| 4 | Kept from old | 90-day uptime, weighted Priority Score, full alerts, runbooks+rollback |
| 5 | Downtime Prediction | **Kept** (full ML + prototype panel) |

## D. Added (new vs prototype) — the build gaps
Mock Controller page · XAI/SHAP card · ML anomaly display · Optimization Impact Forecast
(cost/energy/carbon) · Issues List + Issue/Recommendation Detail · dimension matrix heatmap ·
Audit Log page · missing-monitoring detection+NBA · ticketing/notification connectors ·
telemetry-ingest + module-flow APIs · new fields (region, owner_team, latency_ms, carbon_intensity).

## E. Consciously NOT dropped (preserved from old/prototype)
AI Downtime Prediction · 90-day uptime bar · weighted Priority Score · full alert system
(suppression/retry/SLA) · detailed runbooks + rollback/verification · consolidated incident summary
· post-incident report depth · approval queue.

## F. Source folders status
`md_file_old/` and `hilti_cloud_intelligence_docs/` are now **archive/reference**. Build against
`reconciled_sdd/`. If a requirement conflicts, this folder wins.
