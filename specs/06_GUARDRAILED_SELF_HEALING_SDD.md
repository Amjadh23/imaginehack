# 06 — SDD: Module 3, Guardrailed Self-Healing

## 1. Purpose

Receive a `Recommendation`, decide **auto-fix / approval / escalation** via rules, execute through
simulated MCP connectors, verify, roll back on failure, and report. **Fixes responsibly.**

## 2. Execution sequence (kept from old spec)

```text
Monitor → Diagnose → Select runbook → Check policy → Execute → Verify → Log → Rollback or Escalate on failure
```

## 3. Execution paths

- **Auto-Fix** — low-risk, reversible, non-production.
- **User-Approved Fix** — AI can execute, but only after approval (Approval Queue).
- **Human Escalation** — AI must not fix (critical prod vuln, sensitive data, irreversible, etc.).

## 4. Safety rules (authoritative — see `13` for full detail)

**Auto-fix allowed only if ALL:** non-production · reversible · no sensitive data · DB not affected ·
network/security policy not affected · criticality low/medium · rollback_note exists.

**Approval required if any:** staging/production · criticality high · affects availability/config/
access policy · requires downtime · reversible-but-sensitive.

**Escalate if any:** critical prod vulnerability · sensitive data exposure · prod DB affected ·
unknown dependency · irreversible · data deletion · low AI confidence.

**Never auto-execute:** delete data · modify prod DB · patch critical prod systems · change prod
security/network policy · irreversible infra changes · unknown dependency risk.

## 5. Runbooks + rollback (kept, detailed)

Predefined runbooks: restart_container, rolling_restart, scale_up, scale_down, stop_idle_staging,
schedule_shutdown, resize_resource, reschedule_batch, restrict_public_access/update_storage_acl,
pull_container_image, recommend_base_image_update, enable_monitoring, create_ticket.

- **Verify** success within 30s of execution (workload returns to healthy).
- On verification failure → **rollback** within 60s, then escalate (notify operator with workload,
  runbook, failure reason).
- Runbook timeout 120s → abort + log + escalate. Rollback timeout 60s → abort + log + escalate.

## 6. Simulated MCP connectors

Do not touch real cloud — they update system state and write logs.

- **Cloud:** stop_resource, schedule_shutdown, resize_resource, restrict_public_access,
  enable_monitoring, reschedule_batch_job, restart_container, scale_up/down.
- **Ticketing:** create_ticket, update_ticket, assign_ticket.
- **Notification:** notify_owner, notify_security_team, notify_devops_team, escalate_to_operator.
- **Audit:** write_audit_log.

## 7. Approval Queue + escalation timers (kept from old spec)

Global queue across workloads, sorted Critical→High→Medium, pulsing dot for Critical. Each item:
workload, action, AI rationale, risk, environment, MCP tools, time-since-request, escalation
countdown. Approve / Deny / Snooze (default 30 min). High-risk approval not received in 15 min →
escalate to next-level operator.

## 8. Output

`Remediation Result` + **Remediation Report** + **Audit Log** entry (schemas in `03`). A report is
generated after **every** completion: auto-fix, approved fix, or escalation.

## 9. Acceptance criteria

Evaluates safety context · chooses auto/approval/escalation correctly · simulates ≥3 action types ·
verifies + rolls back on failure · generates report + audit log · never auto-fixes prohibited
actions · updates issue status + heatmap.
