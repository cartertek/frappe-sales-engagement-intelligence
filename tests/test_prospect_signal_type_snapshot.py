from __future__ import annotations

import json
from pathlib import Path

APP = Path("sales_engagement_intelligence")
MODULE = APP / "sales_engagement_and_intelligence"


def test_qualified_indicator_uses_qualification_status_color_and_filter():
    source = (MODULE / "doctype" / "sei_prospect" / "sei_prospect_list.js").read_text()
    assert (
        "const status_field = doc.lifecycle_status ? 'lifecycle_status' : 'qualification_status';"
        in source
    )
    assert "colors[status] || 'gray'" in source
    assert 'class=\"data-pill btn-xs align-center ellipsis\"' in source
    assert "background-color: var(--green-100)" in source
    assert "indicator-pill ${color}" not in source
    assert "qualification_status(value)" in source
    assert "'Manually Approved': 'background-color: var(--green-100); color: var(--green-700);'" in source
    assert "`${status_field},=,${status}`" in source
    assert "'Qualified': 'green'" in source
    assert "'Qualified': 'background-color: var(--green-100); color: var(--green-700);'" in source
    assert "'Needs Review': 'background-color: var(--yellow-100); color: var(--yellow-700);'" in source
    assert "'Unqualified': 'background-color: var(--gray-100); color: var(--gray-700);'" in source
    assert "'Rejected': 'background-color: var(--red-100); color: var(--red-700);'" in source
    assert "'Do Not Contact': 'background-color: var(--red-100); color: var(--red-700);'" in source


def test_fact_evidence_specificity_is_required():
    fact = json.loads(
        (MODULE / "doctype" / "sei_signal_observed_fact" / "sei_signal_observed_fact.json").read_text()
    )
    fields = {field["fieldname"]: field for field in fact["fields"]}
    assert fields["evidence_specificity"]["reqd"] == 1


def test_prospect_has_synced_signal_type_snapshot():
    prospect = json.loads(
        (MODULE / "doctype" / "sei_prospect" / "sei_prospect.json").read_text()
    )
    fields = {field["fieldname"]: field for field in prospect["fields"]}
    signals = fields["signals"]
    assert signals["fieldtype"] == "Data"
    assert signals["read_only"] == 1
    assert not signals.get("in_standard_filter")

    controller = (MODULE / "doctype" / "sei_signal" / "sei_signal.py").read_text()
    assert "self.sync_prospect_signal_types()" in controller
    assert "self.sync_prospect_signal_types(include_previous=True)" in controller
    assert "def after_delete(self):" in controller

    service = (
        MODULE / "services" / "prospect_signal_type_sync.py"
    ).read_text()
    assert "SELECT DISTINCT s.signal_type, st.playbook, st.research_arena" in service
    assert '"signals"' in service
    assert '"playbooks"' in service
    assert '"arenas"' in service
    assert "update_modified=True" in service
    assert 'frappe.get_doc("SEI Prospect", prospect).notify_update()' in service

    setup = (APP / "setup" / "__init__.py").read_text()
    assert "ensure_prospect_signal_type_sync()" in setup
    assert "sync_all_prospect_signal_types()" in setup
