from __future__ import annotations

import importlib
import sys
import types
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_ROOT = ROOT
PATCH = "sales_engagement_intelligence.patches.v0_0_1.repair_playbook_script_false_rejections"


def _load(monkeypatch, rows):
    updates = []

    class DB:
        @staticmethod
        def table_exists(name):
            return name == "SEI Prospect"

        @staticmethod
        def get_value(doctype, name, fields, as_dict=False):
            row = rows.get(name)
            return types.SimpleNamespace(**row) if row else None

        @staticmethod
        def set_value(doctype, name, values, update_modified=False):
            updates.append((name, values, update_modified))

    frappe = types.ModuleType("frappe")
    frappe.db = DB()
    monkeypatch.setitem(sys.modules, "frappe", frappe)
    monkeypatch.syspath_prepend(str(APP_ROOT))
    sys.modules.pop(PATCH, None)
    return importlib.import_module(PATCH), updates


def bad_state():
    return {
        "lifecycle_status": "Rejected",
        "qualification_status": "Rejected",
        "qualification_explanation": "No eligible signal passed its playbook qualification script.",
        "modified": datetime(2026, 7, 24, 20, 38, 29),
    }


def test_restores_exact_backup_states_for_all_29_victims(monkeypatch):
    module, updates = _load(monkeypatch, {name: bad_state() for name in _victim_names()})
    module.execute()
    assert len(updates) == 29
    restored = {name: values for name, values, _ in updates}
    assert restored["SEI-PROS-2026-00148"]["lifecycle_status"] == "Find Contact"
    assert restored["SEI-PROS-2026-00148"]["qualification_status"] == "Qualified"
    assert restored["SEI-PROS-2026-00073"]["lifecycle_status"] == "Research Complete"
    assert restored["SEI-PROS-2026-00073"]["qualification_status"] == "Needs Review"
    assert restored["SEI-PROS-2026-00073"]["moderate_observed_signal_count"] == 1


def test_skips_any_victim_changed_after_bad_migration(monkeypatch):
    rows = {name: bad_state() for name in _victim_names()}
    rows["SEI-PROS-2026-00148"] = {**bad_state(), "modified": datetime(2026, 7, 25, 1, 0, 0)}
    module, updates = _load(monkeypatch, rows)
    module.execute()
    assert "SEI-PROS-2026-00148" not in {name for name, _, _ in updates}
    assert len(updates) == 28


def _victim_names():
    monkey_frappe = types.ModuleType("frappe")
    monkey_frappe.db = types.SimpleNamespace()
    previous = sys.modules.get("frappe")
    sys.modules["frappe"] = monkey_frappe
    try:
        sys.path.insert(0, str(APP_ROOT))
        sys.modules.pop(PATCH, None)
        module = importlib.import_module(PATCH)
        return set(module.BACKUP_STATE)
    finally:
        if previous is None:
            sys.modules.pop("frappe", None)
        else:
            sys.modules["frappe"] = previous
