# 09 — SDD: ML, Explainability & Forecasting (full stack)

```text
Anomaly detection : Isolation Forest
Explainability    : SHAP / SHAP-style feature contributions
Forecasting       : XGBoost Regressor (cost, energy, carbon — 30 day)
User explanation  : LLM (wording only)
Recommendation    : rule-based NBA (not ML)
Downtime forecast : trend/degradation model (see 08)
```

**Hard rule:** the LLM never makes safety or action decisions.

## 1. Isolation Forest

Unsupervised anomaly detection on unlabelled telemetry. Detects "unusual" workloads; it does
**not** classify issue type (rules do that — see `04`). Features listed in `04 §4`.

## 2. SHAP / SHAP-style

Explains which telemetry features drove the anomaly score. Output schema in `03 §4`
(`xai_explanation`). Framed as contribution, not causality. Fallback: top rule-triggered features,
`method = "rule-based feature contribution fallback"`.

## 3. XGBoost forecasting

Train 3 separate regressors for `predicted_cost_30d`, `predicted_energy_kwh_30d`,
`predicted_carbon_kgco2e_30d`.

**Features:** encoded(workload_type, cloud_service_type, environment, region, workflow_criticality),
cpu, memory, runtime_hours_24h, storage_gb, request_count_24h, error_rate, latency_ms, cost_24h,
energy_kwh_24h, carbon_kgco2e_24h, carbon_intensity, encoded(public_exposure, monitoring_enabled).

## 4. Synthetic training data

Mock team generates historical rows (50–200 per workload):

```text
target_cost_30d        = cost_24h        × 30 × noise
target_energy_kwh_30d  = energy_kwh_24h  × 30 × noise
target_carbon_kgco2e_30d = carbon_kgco2e_24h × 30 × noise
noise ∈ [0.85, 1.20]   (inflate for issue scenarios to simulate waste)
```

## 5. Optimization Impact Forecast

XGBoost = baseline (no action). Module 2 applies optimization factor (table in `05 §7`) to get the
after-action forecast and projected savings.

## 6. Fallbacks (must keep output schema)

- XGBoost not ready → formula forecast, `model_name = "deterministic_forecast_fallback"`.
- SHAP not ready → rule-based contribution fallback.
- Isolation Forest not ready → rules-only detection (`04 §9`).

## 7. Acceptance criteria

Anomaly score in Issue · SHAP top factors generated · XGBoost predicts 3 targets · projected
savings computed · forecast shows on Recommendation Detail · all fallbacks degrade gracefully.
