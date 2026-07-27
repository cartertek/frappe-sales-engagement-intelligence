from __future__ import annotations

import importlib
import sys
import types

PATCH = "sales_engagement_intelligence.patches.v0_0_1.reorder_playbook_research_arenas"


def _load(monkeypatch, *, exists=True, fields=()):
    updates = []
    cleared = []

    class DB:
        @staticmethod
        def exists(doctype, name):
            assert (doctype, name) == ("DocType", "SEI Playbook")
            return exists

        @staticmethod
        def set_value(doctype, name, fieldname, value, update_modified=False):
            updates.append((doctype, name, fieldname, value, update_modified))

    frappe = types.ModuleType("frappe")
    frappe.db = DB()
    frappe.get_all = lambda *args, **kwargs: list(fields)
    frappe.clear_cache = lambda **kwargs: cleared.append(kwargs)
    monkeypatch.setitem(sys.modules, "frappe", frappe)
    sys.modules.pop(PATCH, None)
    return importlib.import_module(PATCH), updates, cleared


def test_reorders_research_arenas_before_qualification_tab(monkeypatch):
    fields = [
        types.SimpleNamespace(name="tab-overview", fieldname="overview_tab", idx=1),
        types.SimpleNamespace(name="df-arena-section", fieldname="research_arenas_section", idx=9),
        types.SimpleNamespace(name="df-arenas", fieldname="research_arenas", idx=10),
        types.SimpleNamespace(name="df-qualification", fieldname="qualification_tab", idx=8),
    ]
    patch, updates, cleared = _load(monkeypatch, fields=fields)
    patch.execute()
    values = {name: value for _, name, _, value, _ in updates}
    assert values["df-arena-section"] == 8
    assert values["df-arenas"] == 9
    assert values["df-qualification"] == 10
    assert cleared == [{"doctype": "SEI Playbook"}]


def test_patch_is_noop_without_playbook_doctype(monkeypatch):
    patch, updates, cleared = _load(monkeypatch, exists=False)
    patch.execute()
    assert updates == []
    assert cleared == []
