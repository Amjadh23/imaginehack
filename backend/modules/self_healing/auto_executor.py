"""Auto-fix executor for Module 3 (Guardrailed Self-Healing).

When the NBA pipeline generates a recommendation whose safe path is ``auto_fix``,
this component immediately self-executes the remediation through the shared
:func:`backend.modules.self_healing.executor.execute_recommendation` path,
resolving the issue to ``auto_fixed`` with a complete remediation report.

It subscribes to ``RECOMMENDATION_GENERATED`` (idempotent) and ignores any
recommendation that is not ``auto_fix``. Each run is guarded so it only fires
while the originating issue is still open (a manual execute, reset, or
consolidation in the meantime makes it a no-op).
"""

from __future__ import annotations

import asyncio
import logging

from backend.core.event_bus import Event, EventType, event_bus
from backend.modules.self_healing import executor
from backend.services import issue_service, recommendation_service

logger = logging.getLogger("clover.self_healing.auto_executor")

# Issue statuses that mean the issue has already been handled, so a scheduled
# auto-fix should NOT execute when it fires.
_TERMINAL_STATUSES = frozenset(
    {"auto_fixed", "remediated", "escalated", "rejected", "dismissed"}
)


async def auto_execute(recommendation_id: str) -> bool:
    """Self-execute an ``auto_fix`` recommendation immediately.

    Returns ``True`` if the remediation ran, ``False`` if it was skipped (the
    recommendation vanished or the issue was already handled). Never raises — a
    self-healing failure must not crash the event loop.
    """
    recommendation = recommendation_service.get_recommendation(recommendation_id)
    if recommendation is None:
        return False
    if recommendation.get("required_execution_mode") != "auto_fix":
        return False

    issue = issue_service.get_issue(recommendation["issue_id"])
    if issue is None or issue.get("status") in _TERMINAL_STATUSES:
        # Already remediated/reset/consolidated away — nothing to do.
        return False

    try:
        await executor.execute_recommendation(
            recommendation, enforce_approval_gate=True
        )
        logger.info("Auto-fix executed for recommendation %s", recommendation_id)
        return True
    except Exception:  # noqa: BLE001 - self-healing must never crash the loop
        logger.exception("Auto-fix failed for recommendation %s", recommendation_id)
        return False


async def _on_recommendation_generated(event: Event) -> None:
    """Immediately auto-fix ``auto_fix`` recommendations."""
    payload = event.payload or {}
    recommendation = payload.get("recommendation") or {}
    if recommendation.get("required_execution_mode") != "auto_fix":
        return
    recommendation_id = recommendation.get("recommendation_id")
    if not recommendation_id:
        return
    # Run on the next loop tick (not inline) to avoid re-entrant event dispatch;
    # auto_execute owns its own guards.
    asyncio.create_task(auto_execute(recommendation_id))


_subscribed = False


def register_subscriptions() -> None:
    """Subscribe the auto-executor to ``RECOMMENDATION_GENERATED`` (idempotent)."""
    global _subscribed
    if _subscribed:
        return
    event_bus.subscribe(
        EventType.RECOMMENDATION_GENERATED, _on_recommendation_generated
    )
    _subscribed = True
    logger.info("Auto-fix executor subscribed to RECOMMENDATION_GENERATED")


def unregister_subscriptions() -> None:
    """Detach the subscription (used in tests)."""
    global _subscribed
    if not _subscribed:
        return
    event_bus.unsubscribe(
        EventType.RECOMMENDATION_GENERATED, _on_recommendation_generated
    )
    _subscribed = False
