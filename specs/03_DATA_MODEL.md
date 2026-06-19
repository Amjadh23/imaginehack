# 03 — Unified Data Model

Decision: **Unified model.** One canonical `Workload` entity carries the telemetry→issue→
recommendation→remediation pipeline (new docs) AND the resource findings, scores, runbooks,
and alerts (old spec). "Server" / "resource" / "workload" are the same entity — we use
**workload** as the canonical term, `workload_id` as the key.

---

## 1. Canonical entity graph

```text
Workload
 ├─ TelemetrySnapshot[]      (time-series; latest drives the dashboard)
 ├─ Issue[]                  (detection output: anomaly + SHAP + classification)
 │    └─ Recommendation      (NBA + XGBoost forecast)
 │         └─ Remediation    (execution path + report + audit)
 ├─ SecurityFinding[]        (kept from old spec)
 ├─ GreenOpsFinding[]        (kept from old spec)
 ├─ PriorityScore           (6-factor weighted; drives composite heatmap)
 ├─ DimensionScores         (security/energy/carbon/cost/performance/monitoring; drives matrix)
 ├─ DowntimePrediction      (kept; probability, TTF, timeline)
 ├─ Alert[]                 (kept; suppression/retry/SLA)
 └─ UptimeHistory           (kept; 90-day segments)
```

---

## 2. Workload

```jsonc
{
  "workload_id": "wl-bim-processor-001",
  "workload_name": "BIM Processing Engine",
  "workload_type": "BIM Processing Job",        // business type
  "cloud_service_type": "container",            // vm|container|database|storage|serverless|pipeline
  "environment": "development",                 // production|staging|testing|development
  "region": "ap-southeast-1",
  "owner_team": "Construction Analytics Team",
  "construction_workflow": "bim_model_data_processing",
  "workflow_criticality": "medium",             // critical|high|medium|low
  "status": "healthy"                           // healthy|warning|critical|unreachable
}
```

`construction_workflow` ∈ { field_worker_mobile_app, project_management_dashboard,
iot_equipment_monitoring, bim_model_data_processing, site_safety_analytics, reporting_worker,
customer_order_platform, construction_document_management, site_progress_tracking_system }.
Criticality defaults from a configurable workflow→criticality table.

## 3. TelemetrySnapshot (Module 1 input)

```jsonc
{
  "workload_id": "wl-bim-processor-001",
  "cpu_usage_percent": 3.2, "memory_usage_percent": 18.5, "storage_gb": 250,
  "runtime_hours_24h": 24, "request_count_24h": 120,
  "error_rate_percent": 0.5, "latency_ms": 180,
  "public_exposure": false, "public_storage": false,
  "vulnerability_severity": "none",             // none|low|medium|high|critical
  "critical_vulnerability_count": 0,
  "access_anomaly_detected": false, "monitoring_enabled": true,
  "cost_per_hour": 2.40, "cost_24h": 57.60, "cost_30d_forecast": 1728.00,
  "energy_kwh_24h": 38.5, "carbon_kgco2e_24h": 21.7, "carbon_intensity_gco2_per_kwh": 563,
  "timestamp": "2026-06-20T10:30:00Z"
}
```

Bounds (validated on ingest): cpu/mem/storage/error_rate ∈ [0,100]; counts ≥ 0;
cost ∈ [0, 999999.99]; runtime to 2 dp.

## 4. Issue (Module 1 output / Module 2 input)

```jsonc
{
  "issue_id": "iss-0001", "workload_id": "wl-bim-processor-001",
  "issue_type": "overprovisioned_workload",
  "issue_category": "cost_energy_carbon",       // security|cost|energy|carbon|performance|monitoring
  "severity": "medium", "confidence_score": 0.91,
  "detected_evidence": { "cpu_usage_percent": 3.2, "runtime_hours_24h": 24, "cost_24h": 57.6 },
  "ml_result": { "model_name": "Isolation Forest", "anomaly_score": -0.71, "is_anomaly": true },
  "xai_explanation": {
    "method": "SHAP-style feature contribution",
    "top_contributing_factors": [
      { "feature": "cpu_usage_percent", "value": 3.2, "impact": "Low CPU → idle pattern" },
      { "feature": "runtime_hours_24h", "value": 24, "impact": "Continuous runtime → waste" }
    ]
  },
  "llm_user_explanation": "The BIM Processing Engine appears overprovisioned because ...",
  "estimated_impact": { "cost_risk": "high", "energy_risk": "medium", "carbon_risk": "medium",
                        "security_risk": "low", "workflow_disruption_risk": "low" },
  "status": "new",                              // new|recommended|pending_approval|approved|auto_fixed|remediated|escalated|rejected|dismissed
  "detected_at": "2026-06-20T10:31:00Z"
}
```

## 5. Recommendation (Module 2 output / Module 3 input)

```jsonc
{
  "recommendation_id": "rec-0001", "issue_id": "iss-0001", "workload_id": "wl-bim-processor-001",
  "recommended_action": "Schedule shutdown outside working hours and resize the container.",
  "action_category": "cost_energy_carbon_optimization",
  "recommendation_type": "shutdown_schedule_and_resize",
  "rule_triggered": { "rule_id": "RULE-COST-ENERGY-001", "conditions_matched": ["cpu<10","runtime>=20","non-prod"] },
  "forecast_model_result": { "model_name": "XGBoost Regressor",
    "predicted_cost_30d": 1728.0, "predicted_energy_kwh_30d": 1155.0, "predicted_carbon_kgco2e_30d": 651.0 },
  "optimization_impact_forecast": {
    "forecast_without_action": { "cost_30d": 1728.0, "energy_30d_kwh": 1155.0, "carbon_30d_kgco2e": 651.0 },
    "forecast_after_action":   { "cost_30d": 778.0,  "energy_30d_kwh": 585.0,  "carbon_30d_kgco2e": 330.5 },
    "projected_savings":       { "cost_30d": 950.0,  "energy_30d_kwh": 570.0,  "carbon_30d_kgco2e": 320.5 }
  },
  "risk_level": "low",                          // low|medium|high|critical
  "required_execution_mode": "auto_fix",        // auto_fix|user_approval_required|human_escalation_required
  "approval_required": false,
  "mcp_tools": ["schedule_shutdown","resize_resource"],   // selectable for approval cases
  "llm_recommendation_explanation": "...", "rollback_note": "...", "created_at": "..."
}
```

## 6. Remediation Result + Report

```jsonc
{
  "remediation_id": "rem-0001", "recommendation_id": "rec-0001", "issue_id": "iss-0001",
  "workload_id": "wl-bim-processor-001",
  "execution_path": "auto_fix", "execution_status": "completed",  // not_started|pending_approval|in_progress|completed|failed|escalated|rejected
  "action_taken": { "action_name": "...", "action_details": ["..."], "connector_used": "simulated_cloud_connector" },
  "reason_for_action": "...",
  "safety_decision": { "why_safe": "...", "approval_required": false, "rollback_available": true },
  "ai_decision_steps": [ {"step":"detection","ts":"..."}, {"step":"diagnosis","ts":"..."}, {"step":"policy_check","ts":"..."}, {"step":"execute","ts":"..."}, {"step":"verify","ts":"..."} ],
  "mcp_tools_executed": [ {"tool":"...","category":"...","input":{}, "output":{}, "duration_ms":0, "status":"success"} ],
  "impact_result": { "before": {}, "after": {}, "simulated_savings": {} },
  "execution_timeline": [ {"ts":"...","event":"..."} ],     // ms precision
  "audit_compliance": { "approval_type":"auto", "policy_compliance":"compliant", "rollback_available":true,
                        "retention_expires":"...", "persistent_data_modified":false },
  "user_facing_report": "...",
  "rollback_triggered": false, "verification_result": "passed"
}
```

## 7. Kept old-spec objects

### SecurityFinding
`id, workload_id, construction_workflow, description, severity, recommended_fix, priority_ranking(1–4), detected_at, source(trivy|npm_audit|github_scan|custom)`

### GreenOpsFinding
`id, workload_id, energy_score(0–100), carbon_impact_kg_co2, cost_waste_usd, runtime_waste_hours, remediation_action, improvement_percentage, detected_at`

### PriorityScore (drives composite heatmap) — see `07`
`workload_id, score(0–100,1dp), {6 factor values}, unavailable_factors[], detection_timestamp, computed_at`

### DimensionScores (drives matrix heatmap)
`workload_id, security, energy, carbon, cost, performance, monitoring` — each `{score 0–100, state: green|yellow|red|gray}`

### DowntimePrediction (kept) — see `08`
`workload_id, probability(0–100), estimated_time_to_failure, primary_signal, secondary_signal, pattern_match, confidence(low|medium|high), risk_timeline[12], recommended_preemptive_action?`

### Alert (kept) — see `07`
`id, title, workload_id, construction_workflow, severity, security_impact, energy_impact, cost_impact, recommended_action, self_healing_eligible, status(active|resolved|delivery_failed|suppressed), priority_score, created_at, resolved_at?, resolution_method?, suppressed_until?`

### AuditLog — see `13`
`audit_id, event_type, actor, workload_id, issue_id?, recommendation_id?, remediation_id?, timestamp, previous_status, new_status, details, rollback_note?`

## 8. MCP tool registry (runbooks ↔ connectors)

Each tool declares `category`, `risk_class (high|low)`, `env_scope (production|non_production)`.

| Category | Tools |
|---|---|
| Infrastructure Recovery | restart_container, rolling_restart, scale_up, scale_down, stop_idle_staging, schedule_shutdown, resize_resource, clear_cache |
| Security Response | vulnerability_scan, pull_container_image, update_storage_acl, restrict_public_access, verify_access_policy |
| GreenOps | reschedule_batch, energy_analysis |
| Monitoring | health_check, collect_metrics, enable_monitoring |
| Notification/Ticketing | escalate_to_operator, request_approval, create_ticket, notify_owner, notify_security_team |
| Audit | write_audit_log |
