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
