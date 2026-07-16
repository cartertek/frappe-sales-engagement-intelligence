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
        "primary_contact_name": None,
        "primary_contact_email": None,
        "primary_contact_url": None,
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


def test_qualified_stays_qualified_before_manual_handoff(monkeypatch):
    lifecycle = load_lifecycle_module(monkeypatch)

    assert (
        lifecycle.suggest_lifecycle_status_for_doc(
            prospect(
                qualification_status="Qualified",
                lifecycle_status="Needs Research",
                primary_contact_email="buyer@example.com",
            )
        )
        == "Qualified"
    )


def test_qualified_without_manual_handoff_stays_qualified(monkeypatch):
    lifecycle = load_lifecycle_module(monkeypatch)

    assert (
        lifecycle.suggest_lifecycle_status_for_doc(
            prospect(qualification_status="Qualified", lifecycle_status="Qualified")
        )
        == "Qualified"
    )


def test_find_contact_without_contact_stays_find_contact(monkeypatch):
    lifecycle = load_lifecycle_module(monkeypatch)

    assert (
        lifecycle.suggest_lifecycle_status_for_doc(
            prospect(qualification_status="Qualified", lifecycle_status="Find Contact")
        )
        == "Find Contact"
    )


def test_approved_handoff_with_contact_maps_to_ready_for_crm_conversion(monkeypatch):
    lifecycle = load_lifecycle_module(monkeypatch)

    assert (
        lifecycle.suggest_lifecycle_status_for_doc(
            prospect(
                qualification_status="Qualified",
                lifecycle_status="Find Contact",
                primary_contact_email="buyer@example.com",
            )
        )
        == "Ready for CRM Conversion"
    )



def test_apply_lifecycle_promotes_find_contact_and_syncs_ready_flag(monkeypatch):
    lifecycle = load_lifecycle_module(monkeypatch)
    doc = prospect(
        qualification_status="Qualified",
        lifecycle_status="Find Contact",
        primary_contact_email="buyer@example.com",
        ready_for_crm_conversion=0,
    )

    result = lifecycle.apply_lifecycle_to_doc(doc)

    assert result == {
        "old_lifecycle_status": "Find Contact",
        "lifecycle_status": "Ready for CRM Conversion",
    }
    assert doc.lifecycle_status == "Ready for CRM Conversion"
    assert doc.ready_for_crm_conversion == 1

def test_crm_readiness_requirements_report_met_and_unmet_checks(monkeypatch):
    lifecycle = load_lifecycle_module(monkeypatch)

    requirements = lifecycle.get_crm_readiness_requirements(
        prospect(
            qualification_status="Unqualified",
            lifecycle_status="Do Not Contact",
            do_not_contact=1,
            crm_lead="CRM-LEAD-1",
        )
    )

    by_key = {requirement["key"]: requirement["met"] for requirement in requirements}
    assert by_key == {
        "qualified": False,
        "not_do_not_contact": False,
        "not_protected_lifecycle": False,
        "no_crm_lead": False,
    }

def test_pre_crm_handoff_status_recomputes_from_current_state(monkeypatch):
    lifecycle = load_lifecycle_module(monkeypatch)

    assert lifecycle.suggest_pre_crm_handoff_status(
        prospect(qualification_status="Qualified", lifecycle_status="Find Contact")
    ) == "Qualified"
    assert lifecycle.suggest_pre_crm_handoff_status(
        prospect(qualification_status="Needs Review", lifecycle_status="Find Contact")
    ) == "Research Complete"
    assert lifecycle.suggest_pre_crm_handoff_status(
        prospect(qualification_status="Unqualified", lifecycle_status="Find Contact")
    ) == "New"
    assert lifecycle.suggest_pre_crm_handoff_status(
        prospect(
            qualification_status="Unqualified",
            lifecycle_status="Find Contact",
            signal_summary="Research in progress",
        )
    ) == "Needs Research"

def test_rejected_qualification_maps_to_rejected_lifecycle(monkeypatch):
    lifecycle = load_lifecycle_module(monkeypatch)

    doc = prospect(
        qualification_status="Rejected",
        lifecycle_status="Needs Research",
        last_researched_date="2026-07-16",
        signal_summary="Research completed before rejection.",
        ready_for_crm_conversion=1,
    )

    result = lifecycle.apply_lifecycle_to_doc(doc)

    assert result == {"old_lifecycle_status": "Needs Research", "lifecycle_status": "Rejected"}
    assert doc.lifecycle_status == "Rejected"
    assert doc.qualification_status == "Rejected"
    assert doc.ready_for_crm_conversion == 0
