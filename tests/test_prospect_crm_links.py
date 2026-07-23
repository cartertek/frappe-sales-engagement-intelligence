import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROSPECT_DIR = (
    ROOT
    / "sales_engagement_intelligence"
    / "sales_engagement_and_intelligence"
    / "doctype"
    / "sei_prospect"
)
SCRIPT = (PROSPECT_DIR / "sei_prospect.js").read_text()
API = (
    ROOT
    / "sales_engagement_intelligence"
    / "sales_engagement_and_intelligence"
    / "api.py"
).read_text()
META = json.loads((PROSPECT_DIR / "sei_prospect.json").read_text())


def test_crm_links_use_frontend_routes_and_multi_record_api():
    assert "function crm_frontend_route" in SCRIPT
    assert "'CRM Organization': 'organizations'" in SCRIPT
    assert "get_linked_crm_records" in SCRIPT
    assert 'row.get("crm_contact")' in API
    assert 'filters={"sei_prospect": prospect}' in API


def test_crm_links_open_in_the_current_tab():
    assert 'target="_blank"' not in SCRIPT
    assert "target='_blank'" not in SCRIPT


def test_visible_crm_links_are_html_not_single_link_inputs():
    fields = {field["fieldname"]: field for field in META["fields"] if "fieldname" in field}
    assert fields["crm_links_html"]["fieldtype"] == "HTML"
    assert "crm_lead" not in fields
    for name in ("crm_deal", "crm_organization", "crm_contact"):
        assert fields[name]["hidden"] == 1
