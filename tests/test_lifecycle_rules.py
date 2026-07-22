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
    frappe.db = types.SimpleNamespace(
        exists=lambda *args, **kwargs: False,
        get_value=lambda *args, **kwargs: "Hiring Gap",
        sql=lambda *args, **kwargs: [types.SimpleNamespace(value="Hiring Gap")],
    )
    frappe.get_all = lambda *args, **kwargs: [
        types.SimpleNamespace(contact_role="CTO", signal_specific_relevance=0)
    ]
    frappe.get_doc = lambda *args, **kwargs: None

    model = types.ModuleType("frappe.model")
    document = types.ModuleType("frappe.model.document")
    document.Document = object

    monkeypatch.setitem(sys.modules, "frappe", frappe)
    monkeypatch.setitem(sys.modules, "frappe.model", model)
    monkeypatch.setitem(sys.modules, "frappe.model.document", document)

    contacts_module = (
        "sales_engagement_intelligence.sales_engagement_and_intelligence.services.contacts"
    )
    module_name = "sales_engagement_intelligence.sales_engagement_and_intelligence.services.lifecycle"
    sys.modules.pop(contacts_module, None)
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
        "contacts": [],
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
                contacts=[
                    Prospect(
                        contact_name="Buyer", contact_role="CTO", emails="buyer@example.com", is_primary=1
                    )
                ],
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


def test_find_contact_with_name_only_primary_contact_stays_find_contact(monkeypatch):
    lifecycle = load_lifecycle_module(monkeypatch)

    assert (
        lifecycle.suggest_lifecycle_status_for_doc(
            prospect(
                qualification_status="Qualified",
                lifecycle_status="Find Contact",
                contacts=[Prospect(contact_name="Buyer", contact_role="CTO", emails="", is_primary=1)],
            )
        )
        == "Find Contact"
    )


def test_find_contact_with_email_for_non_playbook_role_stays_find_contact(monkeypatch):
    lifecycle = load_lifecycle_module(monkeypatch)

    assert (
        lifecycle.suggest_lifecycle_status_for_doc(
            prospect(
                qualification_status="Qualified",
                lifecycle_status="Find Contact",
                contacts=[
                    Prospect(
                        contact_name="Buyer",
                        contact_role="Unrelated Role",
                        emails="buyer@example.com",
                        is_primary=1,
                    )
                ],
            )
        )
        == "Find Contact"
    )


def test_ready_status_without_primary_contact_email_returns_to_find_contact(monkeypatch):
    lifecycle = load_lifecycle_module(monkeypatch)

    assert (
        lifecycle.suggest_lifecycle_status_for_doc(
            prospect(
                qualification_status="Qualified",
                lifecycle_status="Ready for CRM Conversion",
                contacts=[Prospect(contact_name="Buyer", contact_role="CTO", emails="", is_primary=1)],
            )
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
                contacts=[
                    Prospect(
                        contact_name="Buyer", contact_role="CTO", emails="buyer@example.com", is_primary=1
                    )
                ],
            )
        )
        == "Ready for CRM Conversion"
    )


def test_apply_lifecycle_promotes_find_contact_and_syncs_ready_flag(monkeypatch):
    lifecycle = load_lifecycle_module(monkeypatch)
    doc = prospect(
        qualification_status="Qualified",
        lifecycle_status="Find Contact",
        contacts=[
            Prospect(contact_name="Buyer", contact_role="CTO", emails="buyer@example.com", is_primary=1)
        ],
    )

    result = lifecycle.apply_lifecycle_to_doc(doc)

    assert result == {
        "old_lifecycle_status": "Find Contact",
        "lifecycle_status": "Ready for CRM Conversion",
    }
    assert doc.lifecycle_status == "Ready for CRM Conversion"


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

    assert (
        lifecycle.suggest_pre_crm_handoff_status(
            prospect(qualification_status="Qualified", lifecycle_status="Find Contact")
        )
        == "Qualified"
    )
    assert (
        lifecycle.suggest_pre_crm_handoff_status(
            prospect(qualification_status="Needs Review", lifecycle_status="Find Contact")
        )
        == "Research Complete"
    )
    assert (
        lifecycle.suggest_pre_crm_handoff_status(
            prospect(qualification_status="Unqualified", lifecycle_status="Find Contact")
        )
        == "New"
    )
    assert (
        lifecycle.suggest_pre_crm_handoff_status(
            prospect(
                qualification_status="Unqualified",
                lifecycle_status="Find Contact",
                signal_summary="Research in progress",
            )
        )
        == "Needs Research"
    )


def test_rejected_qualification_maps_to_rejected_lifecycle(monkeypatch):
    lifecycle = load_lifecycle_module(monkeypatch)

    doc = prospect(
        qualification_status="Rejected",
        lifecycle_status="Needs Research",
        last_researched_date="2026-07-16",
        signal_summary="Research completed before rejection.",
    )

    result = lifecycle.apply_lifecycle_to_doc(doc)

    assert result == {"old_lifecycle_status": "Needs Research", "lifecycle_status": "Rejected"}
    assert doc.lifecycle_status == "Rejected"
    assert doc.qualification_status == "Rejected"


def configure_persistence(monkeypatch, lifecycle, doc):
    writes = []
    doc.notify_update = lambda: None
    lifecycle.frappe.get_doc = lambda *args: doc
    lifecycle.frappe.db.set_value = lambda *args, **kwargs: writes.append((args, kwargs))
    return writes


def test_mark_ready_enters_find_contact_without_primary_contact(monkeypatch):
    lifecycle = load_lifecycle_module(monkeypatch)
    doc = prospect(qualification_status="Qualified", lifecycle_status="Qualified")
    writes = configure_persistence(monkeypatch, lifecycle, doc)

    result = lifecycle.mark_ready_for_crm_conversion(doc.name)

    assert result == {"lifecycle_status": "Find Contact"}
    assert writes[0][0][2:] == ("lifecycle_status", "Find Contact")


def test_mark_ready_enters_find_contact_with_name_only_primary_contact(monkeypatch):
    lifecycle = load_lifecycle_module(monkeypatch)
    doc = prospect(
        qualification_status="Qualified",
        lifecycle_status="Qualified",
        contacts=[Prospect(contact_name="Buyer", emails="", is_primary=1)],
    )
    writes = configure_persistence(monkeypatch, lifecycle, doc)

    result = lifecycle.mark_ready_for_crm_conversion(doc.name)

    assert result == {"lifecycle_status": "Find Contact"}
    assert writes[0][0][2:] == ("lifecycle_status", "Find Contact")


def test_mark_ready_enters_find_contact_for_email_on_non_playbook_role(monkeypatch):
    lifecycle = load_lifecycle_module(monkeypatch)
    doc = prospect(
        qualification_status="Qualified",
        lifecycle_status="Qualified",
        contacts=[
            Prospect(
                contact_name="Buyer",
                contact_role="Unrelated Role",
                emails="buyer@example.com",
                is_primary=1,
            )
        ],
    )
    writes = configure_persistence(monkeypatch, lifecycle, doc)

    result = lifecycle.mark_ready_for_crm_conversion(doc.name)

    assert result == {"lifecycle_status": "Find Contact"}
    assert writes[0][0][2:] == ("lifecycle_status", "Find Contact")


def test_mark_ready_enters_ready_status_with_usable_primary_contact(monkeypatch):
    lifecycle = load_lifecycle_module(monkeypatch)
    doc = prospect(
        qualification_status="Qualified",
        lifecycle_status="Qualified",
        contacts=[
            Prospect(contact_name="Buyer", contact_role="CTO", emails="buyer@example.com", is_primary=1)
        ],
    )
    writes = configure_persistence(monkeypatch, lifecycle, doc)

    result = lifecycle.mark_ready_for_crm_conversion(doc.name)

    assert result == {"lifecycle_status": "Ready for CRM Conversion"}
    assert writes[0][0][2:] == ("lifecycle_status", "Ready for CRM Conversion")


def test_mark_ready_returns_original_readiness_checklist_when_blocked(monkeypatch):
    lifecycle = load_lifecycle_module(monkeypatch)
    doc = prospect(
        qualification_status="Unqualified",
        lifecycle_status="Do Not Contact",
        do_not_contact=1,
        crm_lead="CRM-LEAD-1",
    )
    writes = configure_persistence(monkeypatch, lifecycle, doc)

    result = lifecycle.mark_ready_for_crm_conversion(doc.name)

    assert result["ok"] is False
    assert result["error"]["code"] == "CRM_READINESS_REQUIREMENTS_NOT_MET"
    requirements = {row["key"]: row["met"] for row in result["error"]["details"]["requirements"]}
    assert requirements == {
        "qualified": False,
        "not_do_not_contact": False,
        "not_protected_lifecycle": False,
        "no_crm_lead": False,
    }
    assert writes == []


def test_mark_not_ready_returns_handoff_to_qualified(monkeypatch):
    lifecycle = load_lifecycle_module(monkeypatch)
    doc = prospect(qualification_status="Qualified", lifecycle_status="Ready for CRM Conversion")
    writes = configure_persistence(monkeypatch, lifecycle, doc)

    result = lifecycle.mark_not_ready_for_crm_conversion(doc.name)

    assert result == {"lifecycle_status": "Qualified"}
    assert writes[0][0][2:] == ("lifecycle_status", "Qualified")


def test_mark_not_ready_rejects_non_handoff_status(monkeypatch):
    lifecycle = load_lifecycle_module(monkeypatch)
    doc = prospect(qualification_status="Qualified", lifecycle_status="Qualified")
    writes = configure_persistence(monkeypatch, lifecycle, doc)

    result = lifecycle.mark_not_ready_for_crm_conversion(doc.name)

    assert result["ok"] is False
    assert result["error"]["code"] == "CRM_HANDOFF_NOT_ACTIVE"
    assert writes == []


def test_ready_contact_revalidation_patch_is_registered():
    from pathlib import Path

    patches = Path("sales_engagement_intelligence/patches.txt").read_text()
    source = Path(
        "sales_engagement_intelligence/patches/v0_0_1/revalidate_ready_for_crm_contacts.py"
    ).read_text()

    assert "revalidate_ready_for_crm_contacts" in patches
    assert 'filters={"lifecycle_status": "Ready for CRM Conversion"}' in source
    assert "apply_lifecycle_status(prospect)" in source


def test_signal_specific_role_requires_signal_relevance(monkeypatch):
    lifecycle = load_lifecycle_module(monkeypatch)
    sys.modules["frappe"].get_all = lambda *args, **kwargs: [
        types.SimpleNamespace(contact_role="CTO", signal_specific_relevance=1)
    ]

    without_relevance = prospect(
        qualification_status="Qualified",
        lifecycle_status="Find Contact",
        contacts=[
            Prospect(
                contact_name="Buyer",
                contact_role="CTO",
                emails="buyer@example.com",
                is_primary=1,
                signal_relevance="",
            )
        ],
    )
    with_relevance = prospect(
        qualification_status="Qualified",
        lifecycle_status="Find Contact",
        contacts=[
            Prospect(
                contact_name="Buyer",
                contact_role="CTO",
                emails="buyer@example.com",
                is_primary=1,
                signal_relevance="Owns the hiring initiative behind SIG-001.",
            )
        ],
    )

    assert lifecycle.suggest_lifecycle_status_for_doc(without_relevance) == "Find Contact"
    assert lifecycle.suggest_lifecycle_status_for_doc(with_relevance) == "Ready for CRM Conversion"


def test_general_role_does_not_require_signal_relevance(monkeypatch):
    lifecycle = load_lifecycle_module(monkeypatch)
    sys.modules["frappe"].get_all = lambda *args, **kwargs: [
        types.SimpleNamespace(contact_role="CTO", signal_specific_relevance=0)
    ]

    assert (
        lifecycle.suggest_lifecycle_status_for_doc(
            prospect(
                qualification_status="Qualified",
                lifecycle_status="Find Contact",
                contacts=[
                    Prospect(
                        contact_name="Buyer",
                        contact_role="CTO",
                        emails="buyer@example.com",
                        is_primary=1,
                        signal_relevance="",
                    )
                ],
            )
        )
        == "Ready for CRM Conversion"
    )
