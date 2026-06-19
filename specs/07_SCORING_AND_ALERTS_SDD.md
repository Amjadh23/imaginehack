# 07 — SDD: Scoring & Alerts (kept from old spec)

Cross-cutting engines kept by decision. Scoring drives the **composite heatmap**; dimension scores
drive the **matrix heatmap**; alerts drive notifications.

---

# Part A — Scoring Engine

## A1. Weighted Priority Score

`Priority_Score` ∈ [0,100], 1 dp = normalized weighted sum of six factors:

1. security_severity
2. energy_waste
3. cost_waste
4. workflow_criticality
5. environment_type
6. self_healing_safety

Weights are configurable (`rules/scoring_weights.json`), each ∈ [0,1], summing to 1.0.
**Constraint:** `security_severity` and `environment_type` each ≥ 1.5× the average of the other four.

## A2. Rules

- Deterministic: identical inputs+weights → identical score.
- Tiebreaker: earlier `detection_timestamp` ranks higher.
- Missing factors: redistribute their weight proportionally among available factors; list
  `unavailable_factors`.
- Recalculate within 60s of any underlying metric change.

## A3. Component scores (existing formulas, kept)

- **Security_Score** = max(0, 100 − Σ deductions): Critical −25, High −15, Medium −5, Low −2.
  Risk level: Critical [0–25], High [26–50], Medium [51–75], Low [76–100].
- **Energy_Score** = max(0, 100 − Σ deductions): 5–30 pts per inefficiency, cumulative.
  Energy-critical if < 50.
- **Carbon** = compute_hours × power_draw_kwh × emissions_factor (default 0.5 kg CO₂/kWh), or from
  telemetry `carbon_kgco2e`.

## A4. DimensionScores (matrix heatmap)

Per workload, compute a 0–100 score and green/yellow/red/gray state for each of: **Security,
Energy, Carbon, Cost, Performance, Monitoring**. `gray` = insufficient data.

---

# Part B — Alert System

## B1. Conditions

Critical vulns · publicly exposed services · CPU >90% for >5min · memory >90% for >5min ·
error_rate >5% · idle >12h runtime · Energy_Score <30 · failed status · self-healing failure ·
human approval required · **missing monitoring** (new).

## B2. Severity from Priority_Score

Critical >80 · High >60–80 · Medium >30–60 · Low ≤30.

## B3. Delivery & lifecycle

- Critical delivered within 30s; High/Medium/Low within 5 min.
- Retry 3× at 10s intervals; then mark `delivery_failed`.
- **Suppression:** ≥15 min between duplicate same-condition alerts before a follow-up.
- Auto-resolve within 60s when self-healing clears the condition; record resolution method.

## B4. Required fields

title (≤120) · workload · construction_workflow · severity · security_impact (≤500) ·
energy_impact (≤500) · cost_impact (≤500) · recommended_action · self_healing_eligible · status.

## B5. Acceptance criteria

All conditions fire · severity matches Priority_Score thresholds · suppression + retry work ·
auto-resolve works · all required fields present.
