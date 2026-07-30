import json
from pathlib import Path

ROOT = Path("sales_engagement_intelligence/sales_engagement_and_intelligence/doctype")
PROSPECT = json.loads((ROOT / "sei_prospect/sei_prospect.json").read_text())
TEMPLATE = json.loads((ROOT / "sei_message_template/sei_message_template.json").read_text())
TYPE = json.loads((ROOT / "sei_prospect_type/sei_prospect_type.json").read_text())
PATCH = Path("sales_engagement_intelligence/patches/v0_0_1/seed_prospect_types.py").read_text()
PATCHES = Path("sales_engagement_intelligence/patches.txt").read_text()


def _field(schema, fieldname):
    return next(field for field in schema["fields"] if field["fieldname"] == fieldname)


def test_prospect_type_is_an_app_wide_managed_doctype():
    assert TYPE["name"] == "SEI Prospect Type"
    assert TYPE["autoname"] == "field:prospect_type_name"
    name = _field(TYPE, "prospect_type_name")
    assert name["reqd"] == 1
    assert name["unique"] == 1


def test_single_value_prospect_type_fields_link_to_managed_list():
    for schema in (PROSPECT, TEMPLATE):
        field = _field(schema, "prospect_type")
        assert field["fieldtype"] == "Link"
        assert field["options"] == "SEI Prospect Type"
        assert "\n" not in field["options"]


def test_migration_seeds_only_canonical_prospect_types():
    expected = {"Agency", "Startup", "SMB", "Enterprise", "Nonprofit", "NGO", "Government"}
    for value in expected:
        assert f'"{value}"' in PATCH
    legacy_values = (
        "Ecosystem Partner",
        "Directory Lead",
        "Community Lead",
        "Procurement Lead",
        "Referral Partner",
        "Other",
    )
    for legacy in legacy_values:
        assert f'"{legacy}"' not in PATCH
    assert "seed_prospect_types" in PATCHES
