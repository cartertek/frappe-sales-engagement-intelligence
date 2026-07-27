from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCH_MODULE = (
    "sales_engagement_intelligence.patches.v0_0_1."
    "backfill_default_playbook_qualification_script"
)


def _load_patch(*, table_exists: bool):
    calls = []

    class FakeDB:
        def table_exists(self, doctype):
            calls.append(("table_exists", doctype))
            return table_exists

        def sql(self, query, values=None):
            calls.append(("sql", query, values))

    fake_frappe = types.ModuleType("frappe")
    fake_frappe.db = FakeDB()
    sys.modules["frappe"] = fake_frappe
    sys.path.insert(0, str(ROOT))
    sys.modules.pop(PATCH_MODULE, None)
    return importlib.import_module(PATCH_MODULE), calls


def test_backfill_updates_only_blank_existing_scripts():
    patch, calls = _load_patch(table_exists=True)
    patch.execute()

    sql_calls = [call for call in calls if call[0] == "sql"]
    assert len(sql_calls) == 1
    _, query, value = sql_calls[0]
    assert "UPDATE `tabSEI Playbook`" in query
    assert "signal_qualification_script IS NULL" in query
    assert "TRIM(signal_qualification_script) = ''" in query
    assert value == patch.signal_qualification_script.DEFAULT_SIGNAL_QUALIFICATION_SCRIPT


def test_backfill_is_safe_when_playbook_table_is_missing():
    patch, calls = _load_patch(table_exists=False)
    patch.execute()
    assert not [call for call in calls if call[0] == "sql"]
