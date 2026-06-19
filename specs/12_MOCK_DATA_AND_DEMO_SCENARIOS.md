# 12 — Mock Data & Demo Scenarios

No real HILTI access → synthetic telemetry from a live mock generator/controller. The generator is
critical: it controls what happens during the pitch.

## 1. Generator responsibilities
Create healthy baselines · stream telemetry · trigger issue scenarios · reset to healthy ·
POST to `/api/telemetry/ingest` · provide enough data for Isolation Forest, XGBoost, SHAP, both
heatmaps, issues list, demos.

## 2. Synthetic workloads (≥8)
| ID | Name | Type | Env | Criticality |
|---|---|---|---|---|
| wl-field-app-001 | Field Reporting App API | Field App | production | high |
| wl-iot-dashboard-001 | IoT Monitoring Dashboard | IoT Dashboard | production | high |
| wl-bim-processor-001 | BIM Processing Engine | BIM Job | development | medium |
| wl-doc-storage-001 | Project Document Storage | Storage | production | critical |
| wl-report-generator-001 | Monthly Report Generator | Batch | staging | medium |
| wl-ci-pipeline-001 | Deployment CI/CD Pipeline | Pipeline | development | medium |
| wl-costly-vm-001 | Legacy Analytics VM | VM | testing | low |
| wl-site-db-001 | Site Operations Database | Database | production | critical |

For a richer composite heatmap demo, scale to ~20 workloads (the prototype already shows 20).

## 3. Demo scenarios (trigger → expected behavior)
| Trigger | Target | Expected |
|---|---|---|
| trigger_idle_dev_server | wl-bim-processor-001 | detect idle/overprovisioned → NBA shutdown+resize → **auto-fix** (low-risk) → report w/ cost/energy/carbon savings |
| trigger_public_storage_exposure | wl-doc-storage-001 | detect public storage → NBA restrict+notify → **approval/escalation** (prod/sensitive), no blind fix |
| trigger_critical_production_vulnerability | wl-field-app-001 | detect critical vuln → NBA patch/isolate → **human escalation**, no auto-patch prod |
| trigger_carbon_heavy_batch_job | wl-report-generator-001 | detect carbon-heavy → NBA reschedule/resize → forecast carbon reduction → approval/auto if safe |
| trigger_missing_monitoring | wl-ci-pipeline-001 | detect no monitoring → NBA enable + ticket → auto-ticket/enable if safe |
| trigger_cost_spike | wl-costly-vm-001 | detect cost anomaly → SHAP highlights cost/runtime/util → NBA resize/shutdown → savings forecast |
| trigger_high_error_rate | (any prod) | detect high error rate → NBA investigate/notify → escalation if prod |

Each scenario: full pipeline (detection → scoring → AI → action → dashboard) visibly within ~60s;
repeatable; visible stage transitions.

## 4. Stream + reset
- Manual trigger mode (button → immediate patch) and continuous stream (every 3–10s).
- Reset: clear scenario flags, send healthy telemetry, clear demo issues, heatmap back to green.

## 5. Deliverables (AI/mock subteam)
`sample_workloads.json` · `healthy_telemetry_baseline.json` ·
`historical_telemetry_training_data.csv` (XGBoost) · `scenario_payloads.json` ·
`mock_data_generator_service` · `mock_controller_ui`/endpoints · trigger docs.

## 6. Suggested live demo order
Healthy heatmap → idle dev (auto-fix + savings) → public storage (approval/escalation) →
carbon-heavy batch (carbon reduction) → audit log → close on measurable outcomes. Demo < 5 min.

## 7. Backup plan
Preloaded scenario data + recorded screenshots for dashboard, issue detail, recommendation detail,
approval workflow, remediation report, audit log.
