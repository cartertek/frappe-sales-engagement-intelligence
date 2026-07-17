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
    assert "`${status_field},=,${status}`" in source
    assert "'Qualified': 'green'" in source


def test_signal_evidence_specificity_is_required():
    signal = json.loads(
        (MODULE / "doctype" / "sei_signal" / "sei_signal.json").read_text()
    )
    fields = {field["fieldname"]: field for field in signal["fields"]}
    assert fields["evidence_specificity"]["reqd"] == 1


def test_prospect_has_synced_signal_type_snapshot():
    prospect = json.loads(
        (MODULE / "doctype" / "sei_prospect" / "sei_prospect.json").read_text()
    )
    fields = {field["fieldname"]: field for field in prospect["fields"]}
    signals = fields["signals"]
    assert signals["fieldtype"] == "Data"
    assert signals["read_only"] == 1
    assert signals["in_standard_filter"] == 1

    controller = (MODULE / "doctype" / "sei_signal" / "sei_signal.py").read_text()
    assert "self.sync_prospect_signal_types()" in controller
    assert "self.sync_prospect_signal_types(include_previous=True)" in controller
    assert "def after_delete(self):" in controller

    service = (
        MODULE / "services" / "prospect_signal_type_sync.py"
    ).read_text()
    assert 'filters={"prospect": prospect, "signal_type": ["is", "set"]}' in service
    assert '", ".join(dict.fromkeys(signal_types))' in service
    assert '"signals"' in service

    setup = (APP / "setup" / "__init__.py").read_text()
    assert "ensure_prospect_signal_type_sync()" in setup
    assert "sync_all_prospect_signal_types()" in setup
