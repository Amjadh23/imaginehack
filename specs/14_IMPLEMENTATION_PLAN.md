# 14 — Implementation Plan (phased)

Build order: **Demo backbone → Data flow → Detection → Recommendation → Self-healing → Reports →
Polish.** Start with a working end-to-end product, not the most advanced AI.

This is a maximalist merge — phase ruthlessly. **P0 + Downtime Prediction is a winning demo on its
own.** P2 is stretch.

---

## P0 — Demo-critical (must-have for the pitch)

Gaps the prototype lacks + the spine of the flow.

1. **Backend spine:** FastAPI app, unified `Workload` model, telemetry ingest, SQLite/JSON store,
   event bus, config/policy loaders.
2. **Mock Data Controller** (page + `/api/mock/*`): scenario triggers, stream, reset.
3. **Module 1 detection:** rules first; Isolation Forest + SHAP card.
4. **Module 2 NBA + Optimization Impact Forecast** (XGBoost or formula fallback): cost/energy/carbon
   before-after-savings.
5. **Module 3 guardrailed self-healing:** auto-fix / approval / escalation via simulated connectors
   + remediation report.
6. **UI gaps:** Issues List + Issue/Recommendation Detail (XAI card + Optimization Forecast),
   dimension **matrix heatmap** toggle on the existing composite grid.
7. **Keep + wire:** AI Downtime Prediction panel, 90-day uptime bar (port from prototype).

**P0 done when:** trigger a scenario → issue appears with explanation → recommendation with forecast
→ safe fix/approval/escalation → report + heatmap update, end-to-end in < 60s.

## P1 — Credibility & governance

8. ML wiring polish: Isolation Forest + XGBoost outputs surfaced everywhere; fallbacks proven.
9. **Audit Log page** + audit entries on every event.
10. **Missing-monitoring** detection + NBA path (enable monitoring / create ticket).
11. Ticketing + notification connectors.
12. Real-time WebSocket updates (heatmap colors, approval badge, alerts) + "data stale" indicator.

## P2 — Depth (stretch; kept-from-old-spec)

13. **Weighted Priority Score engine** (6 factors, weight constraints) feeding composite heatmap.
14. **Full Alert system** (suppression, retry, delivery SLAs, auto-resolve).
15. **Runbooks + rollback/verification depth** (timeouts, verify within 30s, rollback within 60s).
16. **Fix prototype bugs:** continuous heatmap gradient; correct Security_Score math
    (2C+1H+2M = 100−(50+15+10)=25, not 28); functional server selector; tooltips on all boxes.
17. Property-based tests for scoring/policy/threshold invariants.

---

## Team split
- **Software eng:** web app, dashboard, backend APIs, storage, workflow pages.
- **AI/mock-data:** synthetic telemetry, mock controller, Isolation Forest, XGBoost, SHAP, LLM
  payloads, scenario data.
- **Pitch:** storyline, demo script, flowchart, slide deck, Q&A, fallback screenshots.

## Suggested file structure
```text
/frontend  (app, components, pages, lib, types)
/backend   (api, modules/{detection_insight,next_best_action,self_healing,forecasting,audit},
            schemas, services, data)
/mock-data-generator (scenarios, streams, controllers)
/ml        (isolation_forest, xgboost_forecast, explainability)
/rules     (detection_rules.json, recommendation_rules.json, safety_rules.json, scoring_weights.json)
/tests     (unit, integration, demo_flows)
```

## Engineering risks
| Risk | Mitigation |
|---|---|
| ML takes too long | rules + formula/template fallbacks (schemas unchanged) |
| LLM unavailable | template explanations |
| Live stream breaks | manual scenario triggers |
| UI not polished | focus on heatmap, issue detail, report |
| Too many features | hold the line at P0; P2 is stretch |
