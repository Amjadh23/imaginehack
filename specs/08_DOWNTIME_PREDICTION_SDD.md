# 08 — SDD: AI Downtime Prediction (KEPT)

Decision: kept on top of the full ML stack. It is the prototype's standout demo panel
(`server-detail.html`) and is preserved as a presentation-layer + engine feature.

## 1. Purpose

Predict when a workload is likely to fail from historical metric trends, so teams can act
preemptively before an unplanned outage.

## 2. Inputs

Historical metric trends per workload: CPU, memory, error_rate, GC pause time (where available),
latency. Window configurable (default 12h).

## 3. Outputs (`DowntimePrediction`)

- `probability` 0–100% of failure within the prediction window.
- `estimated_time_to_failure` (hours/minutes), from degradation rate
  (e.g. memory +X%/hr → projected OOM at Y hrs).
- Contributing signals: `primary_signal`, `secondary_signal`, `pattern_match`
  (similar past incidents), `confidence` (Low/Med/High by count of matching historical events).
- `risk_timeline` — 12-point array (one per hour) of color-coded risk for the timeline bar.
- `recommended_preemptive_action` — generated when probability > 70% (e.g. graceful restart to
  clear a memory leak), with a planned-vs-unplanned downtime comparison.

## 4. Relationship to the other ML

Distinct from Isolation Forest (which flags *current* anomaly). Downtime Prediction is a
*forward* failure forecast. When probability > 70% it feeds Module 2/3 as a preemptive
recommendation that flows through the normal safety gate (usually approval for production).

## 5. UI

- **AI Downtime Prediction panel** on the workload detail Overview (probability, time-to-failure,
  12h risk timeline bar, contributing signals, preemptive-action CTA).
- **Heatmap tooltip** includes predicted downtime risk alongside Priority_Score and status.

## 6. Fallback

If no/short history → return `confidence: low` and suppress the preemptive CTA rather than
fabricating a number.

## 7. Acceptance criteria

Computes probability + time-to-failure + contributing signals + 12h timeline · >70% triggers
preemptive recommendation · panel renders on detail view · tooltip shows risk.
