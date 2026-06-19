# 04 — SDD: Module 1, Detection & Insight

## 1. Purpose

Receive telemetry, detect anomalies/issues, and explain what is wrong and why it matters.
Entry point of intelligence. **Finds and explains the problem.**

## 2. Flow

```text
Telemetry → preprocessing → Isolation Forest anomaly score
  → SHAP / SHAP-style top factors
  → rule-based issue classification
  → severity assignment
  → structured Issue Object
  → LLM (or template) user explanation
```

## 3. Input / Output

- **Input:** `TelemetrySnapshot` (see `03`).
- **Output:** `Issue` object → Scoring Engine, Downtime Prediction, and Module 2.

## 4. Isolation Forest (anomaly)

Unsupervised — telemetry is unlabelled. Detects unusual patterns (low CPU + high runtime,
high cost, high carbon, abnormal error rate, etc.). Output: `anomaly_score`, `is_anomaly`,
approximate confidence.

**Features:** cpu, memory, runtime_hours_24h, storage_gb, request_count_24h, error_rate, latency_ms,
cost_24h, cost_30d_forecast, energy_kwh_24h, carbon_kgco2e_24h, carbon_intensity, plus encoded
environment, cloud_service_type, workflow_criticality, public_exposure, public_storage,
monitoring_enabled, vulnerability_severity.

## 5. Rule-based issue classification

Isolation Forest flags *that* something is abnormal; rules classify *what* it is.

| Rule | issue_type | category |
|---|---|---|
| public_storage = true | public_storage | security |
| public_exposure = true AND vulnerability_severity = critical | critical_exposed_vulnerability | security |
| cpu < 10 AND runtime ≥ 20h AND non-production | idle_or_overprovisioned_workload | cost_energy_carbon |
| carbon_kgco2e_24h high AND batch/BIM/reporting | carbon_heavy_workload | carbon |
| monitoring_enabled = false | no_monitoring | monitoring |
| error_rate_percent high | high_error_rate | performance |
| cost_30d_forecast high AND low utilization | cost_spike_or_waste | cost |

(Thresholds in `rules/detection_rules.json`.) Rules also run independently of the model so
"obvious" issues are caught even if the model is cold.

## 6. Severity logic

| Condition | Severity |
|---|---|
| critical vulnerability in production | critical |
| public storage in production | high/critical |
| high error rate / missing monitoring in production | high |
| idle dev, overprovisioned test, carbon-heavy non-urgent batch | medium |
| minor cost increase | low/medium |

## 7. Explainability (SHAP)

Answer: *which telemetry features made this workload look abnormal/risky?* Output is the
`xai_explanation.top_contributing_factors` array (feature, value, plain-language impact).
Framed as contribution, **not** causal proof. Surfaced as the **XAI Explanation Card** in the UI.

## 8. LLM explanation

Convert ml+xai into a short, plain-language explanation: what's wrong, why it matters, affected
workload + top evidence. No hallucinated detail; does **not** recommend an action (that's Module 2).

## 9. Fallbacks

- Model fails → rule-based detection only; `ml_result.model_name = "fallback_rules_only"`.
- LLM fails → template: `"This workload was flagged for {issue_type} because {top_evidence}. It may affect {impact_area}."`

## 10. Acceptance criteria

Receives telemetry · detects ≥5 issue types · runs Isolation Forest · emits SHAP top factors ·
classifies via rules · produces Issue objects · generates LLM/template explanation · issues appear
in the Issues List.
