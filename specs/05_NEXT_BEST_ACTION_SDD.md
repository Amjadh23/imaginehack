# 05 — SDD: Module 2, Next Best Action

## 1. Purpose

Receive an `Issue` and recommend what to do next, with a projected cost/energy/carbon forecast.
**Answers: what should the team do about this issue?**

## 2. Flow

```text
Issue Object → recommendation rule match → action category → risk level
  → XGBoost 30-day forecast → Optimization Impact Forecast (before/after/savings)
  → execution mode → LLM (or template) explanation → Recommendation Object
```

## 3. Approach

**Rule-based NBA engine** (deterministic, explainable, testable, safe). The LLM explains the
recommendation; it never chooses the action. Rules live in `rules/recommendation_rules.json`.

## 4. Recommendation rules

| Rule | Condition | Recommend | Execution mode |
|---|---|---|---|
| RULE-SEC-001 | public_exposure + vuln=critical | restrict access, patch/isolate, notify security | prod → human escalation; non-prod → user approval |
| RULE-SEC-002 | public_storage = true | restrict storage access, review ACL, notify owner | prod/sensitive → escalation; non-prod → approval |
| RULE-COST-ENERGY-001 | cpu<10 + runtime≥20 + non-prod + cost_30d>threshold | schedule shutdown + resize | auto_fix if safety allows |
| RULE-CARBON-001 | batch/BIM/reporting + carbon high + criticality low/med | reschedule to low-carbon window, resize | auto_fix if non-prod & reversible, else approval |
| RULE-PERF-001 | error_rate high | investigate logs, notify SRE, create incident | prod → escalation; non-prod → approval/ticket |
| RULE-MON-001 | monitoring_enabled = false | enable monitoring, create owner ticket, add to dashboard | auto-create ticket / auto-enable basic monitoring if safe |
| RULE-COST-001 | cost high + low/moderate utilization | review usage, notify owner, resize/shutdown | depends on env + safety |

## 5. Risk level

| Context | Risk |
|---|---|
| non-prod + reversible + low criticality | low |
| staging + reversible + medium criticality | medium |
| production + config change | high |
| production + security + sensitive data; unknown dependency | critical |

## 6. Execution mode

| Risk / context | Mode |
|---|---|
| low, reversible, non-prod | auto_fix |
| medium/high but AI can execute with permission | user_approval_required |
| critical / sensitive / unknown / production incident | human_escalation_required |

## 7. Optimization Impact Forecast (key new feature)

XGBoost predicts the baseline 30-day cost/energy/carbon (no action). Module 2 applies a
recommendation-specific optimization factor:

```text
forecast_after_action = forecast_without_action × optimization_factor
projected_savings      = forecast_without_action − forecast_after_action
```

| Recommendation type | Cost | Energy | Carbon |
|---|--:|--:|--:|
| shutdown_schedule | 0.20–0.45 | 0.20–0.45 | 0.20–0.45 |
| resize_workload | 0.40–0.75 | 0.40–0.75 | 0.40–0.75 |
| shutdown_and_resize | 0.25–0.50 | 0.25–0.50 | 0.25–0.50 |
| reschedule_batch_job | 0.75–0.90 | 0.90–1.00 | 0.60–0.85 |
| enable_monitoring / restrict_access / patch | 1.00 | 1.00 | 1.00 |

Security-only issues may have zero/NA savings. Rendered as the **Optimization Impact Forecast**
card (before vs after vs savings, for all three of cost/energy/carbon).

## 8. Consolidation (kept from old spec)

When multiple issues hit the same workload within a 5-minute window, emit a single **consolidated
incident summary** with one prioritized action plan (already in prototype `server-ai.html`).

## 9. Acceptance criteria

Maps issue→recommendation · sets risk + execution mode · attaches XGBoost forecast +
optimization impact · provides explanation · appears on Issue/Recommendation Detail page.
