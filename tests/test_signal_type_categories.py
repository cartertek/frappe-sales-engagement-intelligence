import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCTYPE_ROOT = (
    ROOT
    / "sales_engagement_intelligence"
    / "sales_engagement_and_intelligence"
    / "doctype"
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def test_signal_type_category_is_managed_reusable_doctype():
    category = load_json(
        DOCTYPE_ROOT
        / "sei_signal_type_category"
        / "sei_signal_type_category.json"
    )
    assert category["name"] == "SEI Signal Type Category"
    assert category["autoname"] == "field:category_name"
    fields = {field["fieldname"]: field for field in category["fields"]}
    assert fields["category_name"]["reqd"] == 1
    assert fields["category_name"]["unique"] == 1
    assert fields["active"]["default"] == 1


def test_signal_type_requires_reusable_category_and_defaults_uncategorized():
    signal_type = load_json(
        DOCTYPE_ROOT / "sei_signal_type" / "sei_signal_type.json"
    )
    fields = {field["fieldname"]: field for field in signal_type["fields"]}
    category = fields["category"]
    assert category["fieldtype"] == "Link"
    assert category["options"] == "SEI Signal Type Category"
    assert category["reqd"] == 1
    assert category["default"] == "Uncategorized"
    assert category["in_list_view"] == 1
    assert category["in_standard_filter"] == 1
    assert signal_type["field_order"].index("category") == (
        signal_type["field_order"].index("description") + 1
    )


def test_migration_creates_default_category_and_backfills_signal_types():
    source = (
        ROOT
        / "sales_engagement_intelligence"
        / "patches"
        / "v0_0_1"
        / "add_signal_type_categories.py"
    ).read_text()
    assert 'DEFAULT_CATEGORY = "Uncategorized"' in source
    assert '"doctype": "SEI Signal Type Category"' in source
    assert "UPDATE `tabSEI Signal Type`" in source
    assert "COALESCE(category, '') = ''" in source


def test_signal_type_categories_are_in_prospecting_navigation():
    sidebar = load_json(
        ROOT / "sales_engagement_intelligence" / "workspace_sidebar" / "prospecting.json"
    )
    assert any(
        item.get("link_to") == "SEI Signal Type Category"
        for item in sidebar["items"]
    )

    setup = (
        ROOT / "sales_engagement_intelligence" / "setup" / "__init__.py"
    ).read_text()
    assert '("SEI Signal Type Category", "Signal Type Categories", "List", "Grey")' in setup
