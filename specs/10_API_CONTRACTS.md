# 10 — API Contracts (merged)

FastAPI, REST + WebSocket. Merges the new docs' telemetry/module-flow APIs with the old design's
dashboard/incident/approval APIs. Consistent envelopes:

```jsonc
// success
{ "success": true, "data": {}, "message": "..." }
// error
{ "error": true, "code": "VALIDATION_ERROR", "message": "...", "details": { "field": "workload_id" } }
```

## 1. Telemetry & workloads
| Method | Endpoint | Purpose |
|---|---|---|
| POST | /api/telemetry/ingest | Ingest one telemetry record → validate, store, trigger detection |
| POST | /api/telemetry/bulk-ingest | Ingest many |
| GET | /api/workloads | List workloads |
| GET | /api/workloads/:id | Workload detail |
| GET | /api/workloads/:id/telemetry | Telemetry history |
| GET | /api/workloads/:id/uptime | 90-day uptime history (kept) |
| GET | /api/workloads/:id/prediction | Downtime prediction (kept) |

## 2. Detection / Issues
| Method | Endpoint | Purpose |
|---|---|---|
| POST | /api/detection/run[/:workloadId] | Run detection |
| GET | /api/issues[?severity=&category=&environment=&status=] | List/filter issues |
| GET | /api/issues/:id | Issue detail (incl. ml_result + xai_explanation) |
| PATCH | /api/issues/:id/status | Update status |

## 3. Recommendations / Forecast
| Method | Endpoint | Purpose |
|---|---|---|
| POST | /api/recommendations/generate/:issueId | Generate NBA |
| GET | /api/recommendations/:id | Recommendation detail (incl. optimization_impact_forecast) |
| POST | /api/forecast/:workloadId | XGBoost forecast |

## 4. Remediation / Approvals
| Method | Endpoint | Purpose |
|---|---|---|
| POST | /api/remediation/evaluate/:recommendationId | Decide safety path |
| POST | /api/remediation/execute/:recommendationId | Execute auto/approved fix |
| GET | /api/remediation/:id/report | Remediation/post-incident report |
| GET | /api/approvals | Global approval queue |
| POST | /api/approvals/:id/approve | Approve (+ optional selected MCP tools) → execute + report |
| POST | /api/approvals/:id/deny | Deny |
| POST | /api/approvals/:id/snooze | Snooze escalation timer |

## 5. Scoring / Alerts / Audit
| Method | Endpoint | Purpose |
|---|---|---|
| GET | /api/scoring/issues | Ranked issues by Priority_Score |
| GET | /api/alerts[?workload_id=] | Active alerts (kept) |
| GET | /api/mcp/log[?workload_id=] | MCP invocation log |
| GET | /api/audit-logs[, /:id, /issues/:issueId/audit-logs] | Audit logs |

## 6. Dashboard
| Method | Endpoint | Purpose |
|---|---|---|
| GET | /api/dashboard/summary | Summary cards (workloads, active/critical issues, projected savings, etc.) |
| GET | /api/dashboard/heatmap/composite | Per-workload Priority_Score (composite grid) |
| GET | /api/dashboard/heatmap/matrix | Per-workload DimensionScores (matrix view) |
| GET | /api/dashboard/savings | Projected cost/energy/carbon savings summary |
| GET | /api/dashboard/recent-actions | Recent remediations |

## 7. Mock controller
| Method | Endpoint | Purpose |
|---|---|---|
| GET | /api/mock/scenarios | List demo scenarios |
| POST | /api/mock/trigger/:scenarioId | Trigger scenario |
| POST | /api/mock/reset | Reset all workloads to healthy |
| POST | /api/mock/stream/start , /stop | Toggle live telemetry stream |
| GET | /api/mock/status | Stream status |

## 8. Realtime
| Method | Endpoint | Purpose |
|---|---|---|
| WS | /ws/events | heatmap color changes, alerts, healing status, approval-count, prediction updates |
