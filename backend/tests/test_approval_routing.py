"""Tests for approval-queue routing of recommendations (Mock Controller fixes).

Two execution modes must land an item in the global approval queue so a human
can act on it:

* ``user_approval_required`` — the operator signs off before execution.
* ``human_escalation_required`` — escalated to a human expert; per product
  decision these are *routed into the approvals queue* too (not a separate
  state) so they are visible and actionable. Previously only
  ``user_approval_required`` was enqueued, so escalations silently vanished.

``auto_fix`` recommendations must NOT be queued (they self-resolve).
"""

from __future__ import annotations

import os
import tempfile
from datetime import datetime, timezone

# --- Configure an isolated temp DB BEFORE importing the app/config -----------
_TMP_DIR = tempfile.mkdtemp(prefix="clover_approval_routing_")
os.environ["CLOVER_DB_PATH"] = os.path.join(_TMP_DIR, "test_clover.db")

from backend.core.config import get_settings  # noqa: E402

get_settings.cache_clear()

import pytest  # noqa: E402

from backend.core.database import init_db  # noqa: E402

init_db()

from backend.modules.next_best_action import nba_pipeline  # noqa: E402
from backend.modules.self_healing.approval_queue import approval_queue  # noqa: E402
from backend.schemas.recommendation import (  # noqa: E402
    ForecastComponent,
    ForecastModelResult,
    OptimizationImpactForecast,
    Recommendation,
    RuleTriggered,
)
from backend.schemas.workload import Workload  # noqa: E402

# Passed explicitly so queueing never depends on a DB lookup (keeps the test
# independent of which temp DB another test module configured at import time).
_WORKLOAD = Workload(
    workload_id="wl-test-001",
    workload_name="Test Workload",
    workload_type="Web App",
    cloud_service_type="container",
    environment="production",
    region="us-east-1",
    owner_team="test-team",
    construction_workflow="customer_order_platform",
    workflow_criticality="high",
    status="healthy",
)


def _make_recommendation(
    *,
    recommendation_id: str,
    required_execution_mode: str,
    risk_level: str = "high",
) -> Recommendation:
    zero = ForecastComponent(cost_30d=0.0, energy_30d_kwh=0.0, carbon_30d_kgco2e=0.0)
    return Recommendation(
        recommendation_id=recommendation_id,
        issue_id=f"iss-{recommendation_id}",
        workload_id="wl-test-001",
        recommended_action="Restrict public access and notify the team.",
        action_category="security",
        recommendation_type="restrict_access",
        rule_triggered=RuleTriggered(
            rule_id="RULE-SEC-001", conditions_matched=["public_exposure"]
        ),
        forecast_model_result=ForecastModelResult(
            model_name="deterministic_forecast_fallback",
            predicted_cost_30d=0.0,
            predicted_energy_kwh_30d=0.0,
            predicted_carbon_kgco2e_30d=0.0,
        ),
        optimization_impact_forecast=OptimizationImpactForecast(
            forecast_without_action=zero,
            forecast_after_action=zero,
            projected_savings=zero,
        ),
        risk_level=risk_level,
        required_execution_mode=required_execution_mode,
        approval_required=required_execution_mode != "auto_fix",
        mcp_tools=["restrict_public_access"],
        llm_recommendation_explanation="Lock it down.",
        rollback_note="Re-open access if needed.",
        created_at=datetime.now(timezone.utc),
    )


@pytest.fixture(autouse=True)
def _clean_queue():
    approval_queue.clear()
    yield
    approval_queue.clear()


def test_user_approval_required_is_queued():
    rec = _make_recommendation(
        recommendation_id="rec-appr", required_execution_mode="user_approval_required"
    )
    nba_pipeline._queue_for_approval(rec, workload=_WORKLOAD)
    assert approval_queue.get("rec-appr") is not None


def test_human_escalation_required_is_queued():
    """Regression: escalations must appear in the approvals queue."""
    rec = _make_recommendation(
        recommendation_id="rec-esc",
        required_execution_mode="human_escalation_required",
    )
    nba_pipeline._queue_for_approval(rec, workload=_WORKLOAD)
    item = approval_queue.get("rec-esc")
    assert item is not None
    assert item.execution_mode == "human_escalation_required"


def test_auto_fix_is_not_queued():
    rec = _make_recommendation(
        recommendation_id="rec-auto",
        required_execution_mode="auto_fix",
        risk_level="low",
    )
    nba_pipeline._queue_for_approval(rec, workload=_WORKLOAD)
    assert approval_queue.get("rec-auto") is None


def test_queue_item_serialises_execution_mode():
    rec = _make_recommendation(
        recommendation_id="rec-ser",
        required_execution_mode="human_escalation_required",
    )
    nba_pipeline._queue_for_approval(rec, workload=_WORKLOAD)
    payload = approval_queue.get("rec-ser").to_dict()
    assert payload["execution_mode"] == "human_escalation_required"
