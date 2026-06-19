# 11 — UI/UX Specification

Pitch-deck-quality cloud-ops dashboard. Dark navy base, teal/green = healthy, yellow/orange =
warning, red/pink = critical. Persistent **Simulation Mode** banner. Persistent header **pending-
approvals badge**. The existing prototype is the visual baseline — extend it, don't restart.

## Navigation
Dashboard · Workloads · Issues · Recommendations · Self-Healing · Reports · Audit Logs ·
Mock Controller. Plus per-workload detail tabs: Overview · Security · GreenOps · AI Recommendations
· Self-Healing · MCP Activity.

## 1. Dashboard / Heatmap landing — BOTH views (decision)
- **Composite grid** (default): one box per workload, continuous green→red gradient by
  Priority_Score; hover tooltip = name, score, status, top alert, **downtime risk**; click → detail.
  ⚠️ Prototype currently uses discrete buckets — change to continuous gradient.
- **Matrix view** (toggle): rows = workloads × cols = Security/Energy/Carbon/Cost/Performance/
  Monitoring; cells green/yellow/red/gray; click cell → relevant tab/issue.
- **Summary bar:** total workloads, active issues, critical issues, avg Security, avg Energy,
  monthly cost, **projected monthly savings**, **projected carbon reduction**, self-heal actions,
  critical workloads. Real-time via WebSocket; "data stale" indicator if refresh > 2 intervals.

## 2. Issues List (NEW page)
Cross-workload table: Issue ID, Workload, Type, Category, Severity, Explanation summary,
Recommended action, Status, Detected time. Filters: severity, category, environment, owner team,
status, execution mode. Row → Issue Detail.

## 3. Issue / Recommendation Detail (NEW page)
Sections: workload summary · severity/category · detection evidence · **ML anomaly result** ·
**XAI / SHAP top factors card** · LLM explanation · Next Best Action · **Optimization Impact
Forecast** (before/after/savings for cost, energy, carbon) · execution mode · CTA
(Auto-fix / Review approval / Escalate / View report).

### XAI Explanation Card (NEW component)
Table of top factors: Factor · Value · Impact (plain language).

### Optimization Impact Forecast (NEW component)
Before vs after vs projected savings for **cost, energy, and carbon** — side-by-side cards + bar/line
chart + savings badge.

## 4. Workload Detail tabs (kept from prototype)
- **Overview:** Server info · key metrics · Priority_Score · **AI Downtime Prediction panel (kept)**
  · **90-day uptime bar (kept)** · active alerts.
- **Security:** findings grouped by severity, drill-down (description, fix, timestamp, source).
- **GreenOps:** energy/carbon/cost-waste metrics + **line-chart** score degradation + inefficiency
  list.
- **AI Recommendations:** consolidated incident summary + individual recommendations with category
  badges (auto/approval/escalation) and selectable MCP tool checkboxes.
- **Self-Healing:** Major (requires approval, AI rationale, risk, selectable MCP tools) / Minor
  (auto-resolved log) / Execution History (incl. failures + rollback) with report links.
- **MCP Activity:** invocation log (timestamp, category, tool, params, result, policy, report link),
  90-day retention note.

## 5. Self-Healing workflow page
Recommendation summary · safety context · execution path (Auto / Approval / Escalation) · approval
requirement · connector/tool used · rollback note · Approve/Reject/Execute.

## 6. Approval Queue (kept)
Global, sorted Critical→High→Medium, pulsing dot for Critical; per item: workload, action,
rationale, risk, environment, MCP tools, time-since, escalation countdown; Approve/Deny/Snooze.

## 7. Remediation / Post-Incident Report (kept)
What happened → AI Decision Process (timestamps) → MCP Tools Executed (full JSON I/O) → Before/After
→ Execution Timeline (ms) → Audit & Compliance. Linked from Self-Healing, MCP Activity, alerts,
Approval Queue.

## 8. Audit Logs (NEW page)
Table: timestamp, event type, actor, workload, issue, previous status, new status, details.

## 9. Mock Data Controller (NEW page)
Buttons: trigger idle dev server · public storage exposure · critical vulnerability · carbon-heavy
batch · cost spike · high error rate · missing monitoring · Reset all · Start/Stop stream.
Shows current stream status.

## 10. Acceptance criteria
Both heatmaps render and toggle · Issues List + Detail with XAI + Optimization Forecast · Downtime
panel + uptime bar present · Self-Healing auto/approval/escalation · report + audit log readable ·
Mock Controller drives the live demo.
