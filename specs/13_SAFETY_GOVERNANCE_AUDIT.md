# 13 — Safety, Governance & Audit

The system behaves as **AI-assisted remediation with human-in-the-loop safety** — not uncontrolled
automation. Safety decisions are **rule-based and authoritative**; the LLM never decides.

## 1. Decision question
For every recommendation: *Can this be safely auto-fixed? Should the user approve first? Should a
human team handle it?* Inputs: environment, workflow criticality, reversibility, sensitive data,
downtime risk, network/security impact, database impact, confidence.

## 2. Auto-fix allowed (ALL must hold)
non-production · not production · reversible · no sensitive data · DB not affected · network/security
policy not affected · criticality low/medium · rollback note exists.
*Examples:* stop idle dev server, schedule shutdown for test workload, resize non-critical dev
container, create ticket, notify owner, apply tag, enable basic monitoring if safe.

## 3. Approval required (any)
staging/production · criticality high · affects availability · modifies config · changes access
policy · requires downtime · reversible but operationally sensitive.
*Examples:* resize production workload, restrict public access, change schedule, schedule patching,
enable prod monitoring, modify alerting policy.

## 4. Human escalation required (any)
critical prod vulnerability · sensitive data exposure · major outage · unknown dependency · may
cause major downtime · irreversible · deletes data · prod DB affected · critical network/security
policy · low AI confidence.

## 5. Prohibited auto actions (never)
delete data · modify prod DB · patch critical prod systems · change critical security/network policy
· irreversible infra changes · act under unknown dependency risk · act under low confidence.

## 6. Audit log (every meaningful event)
Events: telemetry ingested, issue detected, recommendation generated, safety decision, auto-fix
executed, approval requested/accepted/rejected, escalation created, remediation completed/failed,
rollback suggested.
Fields: `audit_id, event_type, actor, workload_id, issue_id?, recommendation_id?, remediation_id?,
timestamp, previous_status, new_status, details, rollback_note?`. Retain ≥ 90 days.

## 7. Remediation report (after auto-fix / approved / escalation)
issue detected · workload · action or escalation · reason · safety decision · approval status ·
connector used · timestamp · before/after forecast · projected savings · rollback/follow-up · audit
link. (Full section list in `11 §7`.)

## 8. Governance UI
Make safety visible: why auto-fix was allowed, why approval/escalation was chosen, what changed,
what did NOT change, how to roll back.

## 9. Acceptance criteria
All actions pass safety rules · no prohibited action auto-executes · approval + escalation flows
exist · audit logs + reports created · UI explains every safety decision.
