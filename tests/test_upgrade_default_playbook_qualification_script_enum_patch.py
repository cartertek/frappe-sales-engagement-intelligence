from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCH = "sales_engagement_intelligence.patches.v0_0_1.upgrade_default_playbook_qualification_script_enum"


def test_upgrade_patch_replaces_only_known_boolean_defaults(monkeypatch):
    sql_calls = []

    class DB:
        @staticmethod
        def table_exists(name):
            return name == "SEI Playbook"

        @staticmethod
        def sql(query, values=None):
            sql_calls.append((query, values))

    frappe = types.ModuleType("frappe")
    frappe.db = DB()
    monkeypatch.setitem(sys.modules, "frappe", frappe)
    monkeypatch.syspath_prepend(str(ROOT))
    sys.modules.pop(PATCH, None)
    module = importlib.import_module(PATCH)
    module.execute()

    assert len(sql_calls) == len(module.OLD_DEFAULT_SCRIPTS)
    for query, values in sql_calls:
        assert "WHERE signal_qualification_script = %s" in query
        assert values[0] == module.signal_qualification_script.DEFAULT_SIGNAL_QUALIFICATION_SCRIPT
        assert values[1] in module.OLD_DEFAULT_SCRIPTS
