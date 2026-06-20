"""Tests for the timed auto-fix executor (Mock Controller fixes).

The auto-executor schedules an ``auto_fix`` recommendation to self-execute after
a countdown. These tests pin its guard logic (mode filter, terminal-issue guard,
missing-recommendation guard) and that it delegates to the shared executor. The
actual remediation/report path is covered by ``test_remediation_api``.
"""

from __future__ import annotations

import asyncio

import pytest

from backend.modules.self_healing import auto_executor


def _patch(monkeypatch, *, rec, issue, on_exec):
    monkeypatch.setattr(
        auto_executor.recommendation_service, "get_recommendation", lambda rid: rec
    )
    monkeypatch.setattr(auto_executor.issue_service, "get_issue", lambda iid: issue)
    monkeypatch.setattr(auto_executor.executor, "execute_recommendation", on_exec)


def test_auto_execute_runs_for_open_auto_fix(monkeypatch):
    calls = []

    async def _fake_exec(rec, *, enforce_approval_gate=True):
        calls.append(rec["recommendation_id"])

    _patch(
        monkeypatch,
        rec={
            "recommendation_id": "rec-1",
            "issue_id": "iss-1",
            "required_execution_mode": "auto_fix",
        },
        issue={"issue_id": "iss-1", "status": "recommended"},
        on_exec=_fake_exec,
    )
    ran = asyncio.run(auto_executor.auto_execute("rec-1"))
    assert ran is True
    assert calls == ["rec-1"]


def test_auto_execute_skips_non_auto_fix(monkeypatch):
    calls = []

    async def _fake_exec(rec, *, enforce_approval_gate=True):
        calls.append(rec["recommendation_id"])

    _patch(
        monkeypatch,
        rec={
            "recommendation_id": "rec-2",
            "issue_id": "iss-2",
            "required_execution_mode": "user_approval_required",
        },
        issue={"issue_id": "iss-2", "status": "pending_approval"},
        on_exec=_fake_exec,
    )
    ran = asyncio.run(auto_executor.auto_execute("rec-2"))
    assert ran is False
    assert calls == []


@pytest.mark.parametrize("terminal", ["auto_fixed", "remediated", "escalated"])
def test_auto_execute_skips_already_handled_issue(monkeypatch, terminal):
    calls = []

    async def _fake_exec(rec, *, enforce_approval_gate=True):
        calls.append(rec["recommendation_id"])

    _patch(
        monkeypatch,
        rec={
            "recommendation_id": "rec-3",
            "issue_id": "iss-3",
            "required_execution_mode": "auto_fix",
        },
        issue={"issue_id": "iss-3", "status": terminal},
        on_exec=_fake_exec,
    )
    ran = asyncio.run(auto_executor.auto_execute("rec-3"))
    assert ran is False
    assert calls == []


def test_auto_execute_skips_missing_recommendation(monkeypatch):
    monkeypatch.setattr(
        auto_executor.recommendation_service, "get_recommendation", lambda rid: None
    )
    ran = asyncio.run(auto_executor.auto_execute("rec-gone"))
    assert ran is False


def test_auto_execute_swallows_executor_failure(monkeypatch):
    async def _boom(rec, *, enforce_approval_gate=True):
        raise RuntimeError("safety router exploded")

    _patch(
        monkeypatch,
        rec={
            "recommendation_id": "rec-4",
            "issue_id": "iss-4",
            "required_execution_mode": "auto_fix",
        },
        issue={"issue_id": "iss-4", "status": "recommended"},
        on_exec=_boom,
    )
    # Must not raise — self-healing failures stay isolated.
    ran = asyncio.run(auto_executor.auto_execute("rec-4"))
    assert ran is False
