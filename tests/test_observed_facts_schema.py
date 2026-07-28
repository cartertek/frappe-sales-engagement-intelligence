import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "sales_engagement_intelligence"
SIGNAL_JSON = APP / (
    "sales_engagement_and_intelligence/doctype/sei_signal/sei_signal.json"
)
FACT_JSON = APP / (
    "sales_engagement_and_intelligence/doctype/"
    "sei_signal_observed_fact/sei_signal_observed_fact.json"
)
CONTROLLER = APP / (
    "sales_engagement_and_intelligence/doctype/sei_signal/sei_signal.py"
)
QUALIFICATION = APP / "sales_engagement_and_intelligence/services/qualification.py"
API = APP / "sales_engagement_and_intelligence/api.py"


def test_signal_uses_required_observed_facts_child_table():
    signal = json.loads(SIGNAL_JSON.read_text())
    fields = {field["fieldname"]: field for field in signal["fields"]}
    observed_facts = fields["observed_facts"]

    assert "observed_fact" not in fields
    assert observed_facts["fieldtype"] == "Table"
    assert observed_facts["options"] == "SEI Signal Observed Fact"
    assert observed_facts["reqd"] == 1


def test_observed_fact_child_row_is_required_long_text():
    child = json.loads(FACT_JSON.read_text())
    fields = {field["fieldname"]: field for field in child["fields"]}

    assert child["istable"] == 1
    assert fields["fact"]["fieldtype"] == "Long Text"
    assert fields["fact"]["reqd"] == 1


def test_validation_and_qualification_use_full_fact_list():
    controller = CONTROLLER.read_text()
    qualification = QUALIFICATION.read_text()

    assert '_observed_fact_values(self)' in controller
    assert 'signal.get("observed_facts") or []' in qualification
    assert 'data["observed_facts"]' in qualification


def test_api_accepts_and_returns_observed_facts():
    source = API.read_text()

    assert '"observed_facts",' in source
    assert "_normalize_observed_facts" in source
    assert "_attach_observed_facts" in source
