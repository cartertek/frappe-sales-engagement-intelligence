import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "sales_engagement_intelligence/sales_engagement_and_intelligence"


def test_evidence_metadata_lives_only_on_fact_rows():
    signal = json.loads((APP / "doctype/sei_signal/sei_signal.json").read_text())
    child = json.loads((APP / "doctype/sei_signal_observed_fact/sei_signal_observed_fact.json").read_text())
    signal_fields = {row["fieldname"] for row in signal["fields"]}
    child_fields = {row["fieldname"] for row in child["fields"]}
    moved = {"source_url", "source_date", "evidence_basis", "evidence_specificity"}
    assert not (moved & signal_fields)
    assert moved <= child_fields


def test_qualification_uses_fact_level_evidence_basis():
    source = (APP / "services/qualification.py").read_text()
    assert 'item.get("evidence_basis") == "Observed"' in source
    assert 'filters={"prospect": prospect_name, "evidence_basis": "Observed"}' not in source


def test_api_returns_fact_metadata():
    source = (APP / "api.py").read_text()
    for field in ("evidence_basis", "evidence_specificity", "source_url", "source_date"):
        assert f'"{field}": fact.{field}' in source


def test_fact_source_url_is_clickable_and_ui_copy_is_fact_specific():
    child_path = APP / "doctype/sei_signal_observed_fact/sei_signal_observed_fact.json"
    child = json.loads(child_path.read_text())
    fields = {field["fieldname"]: field for field in child["fields"]}
    assert fields["source_url"]["fieldtype"] == "Data"
    assert fields["source_url"]["options"] == "URL"
    assert "this fact" in fields["source_url"]["description"]
    assert "this fact only" in fields["evidence_basis"]["description"]
    assert "this row's source" in fields["evidence_specificity"]["description"]


def test_operator_docs_explain_fact_level_evidence_metadata():
    docs = [
        Path("docs/operator_workflow/README.md"),
        Path("docs/operator_workflow/research_workflow.md"),
        Path("docs/operator_workflow/signal_evaluation.md"),
        Path("docs/assistant_workflows/create-prospect-and-signal.md"),
    ]
    for path in docs:
        source = path.read_text()
        assert "Fact-level evidence metadata" in source
        assert "belong to each Observed Facts row, not to the Signal" in source


def test_fact_grid_wraps_and_uses_half_width():
    child = json.loads((APP / "doctype/sei_signal_observed_fact/sei_signal_observed_fact.json").read_text())
    fields = {field["fieldname"]: field for field in child["fields"]}
    assert fields["fact"]["columns"] == 5
    assert sum(field.get("columns", 0) for field in child["fields"]) == 10

    css = (
        ROOT / "sales_engagement_intelligence/public/css/sales_engagement_intelligence.bundle.css"
    ).read_text()
    assert '[data-fieldname="observed_facts"] .grid-row [data-fieldname="fact"]' in css
    assert "flex: 0 0 50%;" in css
    assert "white-space: pre-wrap;" in css
    assert "height: auto;" in css
    assert "text-overflow: clip;" in css
