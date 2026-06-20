"""Tests that issue consolidation keeps a single active issue per workload.

Per product decision, re-triggering a scenario should update the one active
issue for that workload rather than spawning duplicates — even if the existing
issue was detected long ago. ``find_open_issue`` therefore supports an unbounded
lookup (``within_seconds=None``) which the detector uses for consolidation.
"""

from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timedelta, timezone

# Use a dedicated temp DB passed *explicitly* to every call, so this module is
# immune to the global CLOVER_DB_PATH being reassigned by another test module
# imported later in the same pytest session (a known fragility of these tests).
_TMP_DIR = tempfile.mkdtemp(prefix="clover_consol_age_")
_DB = os.path.join(_TMP_DIR, "test_clover.db")

from backend.core.database import connection, init_db  # noqa: E402
from backend.services import issue_service  # noqa: E402

init_db(_DB)

_WID = "wl-consol-001"


def _seed_workload() -> None:
    with connection(_DB) as conn:
        conn.execute(
            "INSERT OR IGNORE INTO workloads (workload_id, workload_name, "
            "workload_type, cloud_service_type, environment, region, owner_team, "
            "construction_workflow, workflow_criticality, status, data) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                _WID,
                "Consolidation Test",
                "Web App",
                "container",
                "development",
                "eu-central-1",
                "team",
                "bim_model_data_processing",
                "medium",
                "healthy",
                "{}",
            ),
        )


def _insert_open_issue(issue_id: str, *, age_seconds: int) -> None:
    detected = (
        datetime.now(timezone.utc) - timedelta(seconds=age_seconds)
    ).isoformat()
    data = json.dumps({"issue_id": issue_id, "workload_id": _WID})
    with connection(_DB) as conn:
        conn.execute(
            "INSERT INTO issues (issue_id, workload_id, issue_type, issue_category, "
            "severity, status, detected_at, data, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                issue_id,
                _WID,
                "carbon_heavy_workload",
                "carbon",
                "medium",
                "recommended",
                detected,
                data,
                detected,
                detected,
            ),
        )


def test_old_open_issue_is_outside_the_bounded_window():
    _seed_workload()
    _insert_open_issue("iss-old-bounded", age_seconds=3600)
    # The legacy 5-minute window does not see a 1-hour-old issue.
    assert issue_service.find_open_issue(_WID, within_seconds=300, db_path=_DB) is None


def test_unbounded_lookup_finds_old_open_issue():
    """The detector uses within_seconds=None so re-triggers update one issue."""
    found = issue_service.find_open_issue(_WID, within_seconds=None, db_path=_DB)
    assert found is not None
    assert found["issue_id"] == "iss-old-bounded"
