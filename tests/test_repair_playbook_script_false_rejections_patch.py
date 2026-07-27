from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

PATCH = "sales_engagement_intelligence.patches.v0_0_1.repair_playbook_script_false_rejections"
BAD_EXPLANATION = "No eligible signal passed its playbook qualification script."


def _load(monkeypatch, states):
    updates = []

    class DB:
        @staticmethod
        def table_exists(name):
            return name == "SEI Prospect"

        @staticmethod
        def get_value(doctype, name, fields, as_dict=False):
            assert doctype == "SEI Prospect"
            row = states.get(name)
            return types.SimpleNamespace(**row) if row else None

        @staticmethod
        def set_value(doctype, name, values, update_modified=False):
            updates.append((doctype, name, values, update_modified))

    frappe = types.ModuleType("frappe")
    frappe.db = DB()
    monkeypatch.setitem(sys.modules, "frappe", frappe)
    sys.modules.pop(PATCH, None)
    return importlib.import_module(PATCH), updates


def _bad_state():
    return {
        "lifecycle_status": "Rejected",
        "qualification_status": "Rejected",
        "qualification_explanation": BAD_EXPLANATION,
        "modified": "2026-07-24 20:38:29.392884",
    }


def test_repairs_only_backup_verified_victims_with_bad_migration_fingerprint(monkeypatch):
    module, updates = _load(
        monkeypatch,
        {
            "SEI-PROS-2026-00148": _bad_state(),
            "SEI-PROS-2026-00168": _bad_state(),
            "SEI-PROS-2026-00073": _bad_state(),  # changed in migration, but default script would fail
        },
    )
    module.execute()

    by_name = {name: values for _, name, values, _ in updates}
    assert set(by_name) == {"SEI-PROS-2026-00148", "SEI-PROS-2026-00168"}
    assert by_name["SEI-PROS-2026-00148"] == {
        "lifecycle_status": "Find Contact",
        "qualification_status": "Qualified",
        "qualified_signal_count": 1,
        "strong_observed_signal_count": 1,
        "moderate_observed_signal_count": 0,
        "qualification_explanation": "Qualified by 1 strong observed signal.",
    }
    assert by_name["SEI-PROS-2026-00168"]["qualified_signal_count"] == 2
    assert by_name["SEI-PROS-2026-00168"]["moderate_observed_signal_count"] == 2


def test_skips_victim_if_state_changed_after_bad_migration(monkeypatch):
    later = _bad_state()
    later["modified"] = "2026-07-25 12:00:00.000000"
    module, updates = _load(monkeypatch, {"SEI-PROS-2026-00148": later})
    module.execute()
    assert updates == []


def test_backup_verified_victim_set_is_exact():
    module = importlib.import_module(PATCH)
    assert len(module.VICTIMS) == 25
    assert "SEI-PROS-2026-00148" in module.VICTIMS
    assert "SEI-PROS-2026-00073" not in module.VICTIMS
    assert "SEI-PROS-2026-00188" not in module.VICTIMS
