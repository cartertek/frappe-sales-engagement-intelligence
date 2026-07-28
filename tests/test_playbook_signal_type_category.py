import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCTYPE_ROOT = (
    ROOT
    / "sales_engagement_intelligence"
    / "sales_engagement_and_intelligence"
    / "doctype"
)


def test_playbook_signal_type_table_shows_category():
    schema = json.loads(
        (
            DOCTYPE_ROOT
            / "sei_playbook_signal_type"
            / "sei_playbook_signal_type.json"
        ).read_text()
    )
    fields = {field["fieldname"]: field for field in schema["fields"]}
    category = fields["category"]
    assert category["fieldtype"] == "Link"
    assert category["options"] == "SEI Signal Type Category"
    assert category["fetch_from"] == "signal_type.category"
    assert category["read_only"] == 1
    assert category["in_list_view"] == 1
    assert schema["field_order"][:2] == ["signal_type", "category"]


def test_signal_type_sync_updates_playbook_category_snapshot():
    source = (
        DOCTYPE_ROOT / "sei_signal_type" / "sei_signal_type.py"
    ).read_text()
    assert '"category": self.category' in source
    assert '"research_arena": self.research_arena' in source
    assert '"active": self.active' in source


def test_existing_playbook_rows_are_backfilled_from_signal_type():
    source = (
        ROOT
        / "sales_engagement_intelligence"
        / "patches"
        / "v0_0_1"
        / "backfill_playbook_signal_type_categories.py"
    ).read_text()
    assert "UPDATE `tabSEI Playbook Signal Type`" in source
    assert "child.category = signal_type.category" in source
