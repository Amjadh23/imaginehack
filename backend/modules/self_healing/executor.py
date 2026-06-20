"""Shared remediation executor for Module 3 (Guardrailed Self-Healing).

Single source of truth for *running* a stored Recommendation through its safe
path and recording the outcome. Both the remediation API (manual
``POST /execute``) and the auto-fix executor (timed self-healing) call
:func:`execute_recommendation`, so a remediation always produces the same,
fully-populated :class:`RemediationResult` report, advances the originating
issue's status identically, and emits ``REMEDIATION_COMPLETED`` for the audit
recorder / alert resolver / websocket broadcaster.

Centralising this is what guarantees auto-fixed issues get a complete report
(previously only the API path built one) and that the human-approval gate is
enforced consistently.
"""

from __future__ import annotations

import logging

from backend.core.event_bus import Event, EventType, event_bus
from backend.modules.self_healing import report_generator
from backend.modules.self_healing.approval_queue import approval_queue
from backend.schemas.remediation import RemediationResult
from backend.services import (
    issue_service,
    remediation_service,
    workload_service,
)

logger = logging.getLogger("clover.self_healing.executor")


class ApprovalRequiredError(Exception):
    """Raised when a ``user_approval_required`` fix is run before approval.

    Carries the queue ``status_label`` so callers (e.g. the API) can build an
    actionable message without re-querying the queue.
    """

    def __init__(self, recommendation_id: str, status_label: str) -> None:
        self.recommendation_id = recommendation_id
        self.status_label = status_label
        super().__init__(
            f"Remediation {recommendation_id} requires human approval "
            f"(status: {status_label})."
        )


def _is_approved(recommendation_id: str) -> bool:
    item = approval_queue.get(recommendation_id)
    return item is not None and item.status == "approved"


def _advance_issue_status_for_result(result: RemediationResult) -> None:
    """Reflect a completed remediation on its originating issue (best-effort).

    - escalation, or any failed/escalated run -> ``escalated``
    - completed auto-fix                       -> ``auto_fixed``
    - completed approved fix                   -> ``remediated``
    """
    if result.execution_path == "human_escalation" or result.execution_status in (
        "escalated",
        "failed",
    ):
        new_status = "escalated"
    elif result.execution_status == "completed":
        new_status = "auto_fixed" if result.execution_path == "auto_fix" else "remediated"
    else:
        return
    try:
        issue_service.update_status(result.issue_id, new_status)
    except Exception:  # noqa: BLE001 - status write-back is best-effort
        logger.exception(
            "Failed to advance issue %s to %s after remediation",
            result.issue_id,
            new_status,
        )


async def execute_recommendation(
    recommendation: dict,
    *,
    enforce_approval_gate: bool = True,
) -> RemediationResult:
    """Run a recommendation through its safe path, persist + announce the result.

    Steps:
      1. Resolve workload + issue context.
      2. Run the deterministic safety router (``report_generator.evaluate``).
      3. Enforce the human-approval gate for ``user_approval_required`` paths
         (raises :class:`ApprovalRequiredError` unless approved).
      4. Build + persist the full :class:`RemediationResult` report.
      5. Advance the issue's terminal status and emit ``REMEDIATION_COMPLETED``.
    """
    recommendation_id = recommendation["recommendation_id"]
    workload = workload_service.get_workload(recommendation["workload_id"])
    issue = issue_service.get_issue(recommendation["issue_id"])

    decision = report_generator.evaluate(recommendation, workload, issue)
    if (
        enforce_approval_gate
        and decision.execution_path == "user_approval_required"
        and not _is_approved(recommendation_id)
    ):
        item = approval_queue.get(recommendation_id)
        raise ApprovalRequiredError(
            recommendation_id, item.status if item is not None else "not_queued"
        )

    result = report_generator.generate_report(
        recommendation, workload, issue, routing=decision
    )
    remediation_service.create_remediation(result)
    _advance_issue_status_for_result(result)

    await event_bus.publish(
        Event(
            event_type=EventType.REMEDIATION_COMPLETED,
            payload={
                "remediation_id": result.remediation_id,
                "recommendation_id": result.recommendation_id,
                "issue_id": result.issue_id,
                "workload_id": result.workload_id,
                "execution_path": result.execution_path,
                "execution_status": result.execution_status,
            },
        )
    )
    return result
