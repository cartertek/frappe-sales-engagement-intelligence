import json
from pathlib import Path

ROOT = Path("sales_engagement_intelligence/sales_engagement_and_intelligence")
SIGNAL_SCHEMA = json.loads((ROOT / "doctype/sei_signal/sei_signal.json").read_text())
FACT_SCHEMA = json.loads(
    (ROOT / "doctype/sei_signal_observed_fact/sei_signal_observed_fact.json").read_text()
)
SIGNAL_CONTROLLER = (ROOT / "doctype/sei_signal/sei_signal.py").read_text()
SIGNAL_JS = (ROOT / "doctype/sei_signal/sei_signal.js").read_text()
API = (ROOT / "api.py").read_text()
QUALIFICATION = (ROOT / "services/qualification.py").read_text()
TAXONOMY = (ROOT / "services/taxonomy.py").read_text()
DRAFTING = (ROOT / "services/drafting.py").read_text()
LIFECYCLE = (ROOT / "services/lifecycle.py").read_text()
PATCH = Path(
    "sales_engagement_intelligence/patches/v0_0_1/add_signal_draft_status.py"
).read_text()


def test_signal_defaults_to_draft_and_schema_fields_are_optional():
    fields = {field["fieldname"]: field for field in SIGNAL_SCHEMA["fields"]}
    assert fields["status"]["default"] == "Draft"
    assert fields["status"]["options"] == "Draft\nPublished"
    for fieldname in ("signal_name", "prospect", "signal_type", "signal_strength", "observed_facts"):
        assert not fields[fieldname].get("reqd")
    for field in FACT_SCHEMA["fields"]:
        assert not field.get("reqd")


def test_publish_runs_current_required_and_evidence_validation():
    assert "def validate_publishable" in SIGNAL_CONTROLLER
    assert 'if self.status == PUBLISHED:' in SIGNAL_CONTROLLER
    assert 'self.validate_publishable()' in SIGNAL_CONTROLLER
    assert 'self.apply_evidence_guardrails()' in SIGNAL_CONTROLLER
    for label in ("Name", "Prospect", "Signal Type", "Signal Strength", "Observed Facts"):
        assert label in SIGNAL_CONTROLLER
    for label in ("Fact", "Evidence Basis", "Evidence Specificity"):
        assert label in SIGNAL_CONTROLLER


def test_publish_action_and_api_are_explicit():
    assert "add_publish_action(frm)" in SIGNAL_JS
    assert "frm.doc.status !== 'Draft'" in SIGNAL_JS
    assert "publish_signal" in SIGNAL_JS
    assert "def publish_signal(signal: str)" in API
    assert 'doc.status = "Published"' in API
    assert "doc.save()" in API


def test_only_published_signals_feed_downstream_workflows():
    assert '"status": "Published"' in QUALIFICATION
    assert "s.status = 'Published'" in TAXONOMY
    assert '"status": "Published"' in DRAFTING
    assert '"status": "Published"' in LIFECYCLE


def test_existing_signals_are_migrated_to_published():
    assert "UPDATE `tabSEI Signal` SET status = 'Published'" in PATCH

def test_signal_validation_does_not_call_removed_disqualifier_sync():
    assert "sync_disqualifier_check_rows" not in SIGNAL_CONTROLLER
