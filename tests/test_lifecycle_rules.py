from __future__ import annotations

import importlib
import sys
import types


class Prospect(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __setattr__(self, name, value):
        self[name] = value


def load_lifecycle_module(monkeypatch):
    frappe = types.ModuleType("frappe")
    frappe.db = types.SimpleNamespace(exists=lambda *args, **kwargs: False)
    frappe.get_doc = lambda *args, **kwargs: None

    model = types.ModuleType("frappe.model")
    document = types.ModuleType("frappe.model.document")
    document.Document = object

    monkeypatch.setitem(sys.modules, "frappe", frappe)
    monkeypatch.setitem(sys.modules, "frappe.model", model)
    monkeypatch.setitem(sys.modules, "frappe.model.document", document)

    module_name = "sales_engagement_intelligence.sales_engagement_and_intelligence.services.lifecycle"
    sys.modules.pop(module_name, None)
    return importlib.import_module(module_name)


def prospect(**overrides):
    values = {
        "name": "TEST-PROSPECT",
        "do_not_contact": 0,
        "crm_deal": None,
        "crm_lead": None,
        "lifecycle_status": "Needs Research",
        "qualification_status": "Unqualified",
        "last_researched_date": None,
        "signal_summary": None,
        "ready_for_crm_conversion": 0,
    }
    values.update(overrides)
    return Prospect(values)


def test_unqualified_needs_research_stays_needs_research(monkeypatch):
    lifecycle = load_lifecycle_module(monkeypatch)

    assert lifecycle.suggest_lifecycle_status_for_doc(prospect()) == "Needs Research"


def test_unqualified_research_complete_becomes_rejected(monkeypatch):
    lifecycle = load_lifecycle_module(monkeypatch)

    assert (
        lifecycle.suggest_lifecycle_status_for_doc(
            prospect(
                lifecycle_status="Research Complete",
                last_researched_date="2026-07-14",
                signal_summary="No credible outreach signal found.",
            )
        )
        == "Rejected"
    )


def test_apply_lifecycle_aligns_rejected_qualification(monkeypatch):
    lifecycle = load_lifecycle_module(monkeypatch)
    doc = prospect(lifecycle_status="Research Complete", qualification_status="Unqualified")

    result = lifecycle.apply_lifecycle_to_doc(doc)

    assert result == {"old_lifecycle_status": "Research Complete", "lifecycle_status": "Rejected"}
    assert doc.lifecycle_status == "Rejected"
    assert doc.qualification_status == "Rejected"
    assert doc.ready_for_crm_conversion == 0


def test_needs_review_maps_to_research_complete(monkeypatch):
    lifecycle = load_lifecycle_module(monkeypatch)

    assert (
        lifecycle.suggest_lifecycle_status_for_doc(
            prospect(qualification_status="Needs Review", lifecycle_status="Needs Research")
        )
        == "Research Complete"
    )
