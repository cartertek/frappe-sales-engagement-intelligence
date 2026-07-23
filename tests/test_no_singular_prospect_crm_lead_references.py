from pathlib import Path

ROOT = Path("sales_engagement_intelligence/sales_engagement_and_intelligence")
FORBIDDEN = (
    "prospect.crm_lead",
    "frm.doc.crm_lead",
    'prospect.get("crm_lead")',
    "p.crm_lead",
    'doc.get("crm_lead")',
)


def test_production_code_has_no_singular_prospect_crm_lead_references():
    violations = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        if "sei_interaction_attribution" in path.parts:
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        for forbidden in FORBIDDEN:
            if forbidden in text:
                violations.append(f"{path}: {forbidden}")
    assert violations == []
