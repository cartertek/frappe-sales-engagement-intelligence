import json
from pathlib import Path

APP = Path("sales_engagement_intelligence")
MODULE = APP / "sales_engagement_and_intelligence"


def test_prospect_has_queryable_emails_sent_field():
    schema = json.loads((MODULE / "doctype" / "sei_prospect" / "sei_prospect.json").read_text())
    fields = {field["fieldname"]: field for field in schema["fields"]}
    field = fields["emails_sent"]
    assert field["label"] == "Emails Sent"
    assert field["fieldtype"] == "Int"
    assert field["read_only"] == 1
    assert not field.get("in_standard_filter")
    assert schema["field_order"].index("emails_sent") == schema["field_order"].index("message_drafts") + 1


def test_prospect_save_counts_sent_child_rows():
    controller = (MODULE / "doctype" / "sei_prospect" / "sei_prospect.py").read_text()
    service = (MODULE / "services" / "prospect_message_draft_sync.py").read_text()
    assert "self.set_emails_sent()" in controller
    assert "count_sent_message_drafts(self)" in controller
    assert 'row.get("sent")' in service


def test_mark_sent_and_unsent_resynchronize_parent_count():
    api = (MODULE / "api.py").read_text()
    assert api.count("sync_prospect_emails_sent(") >= 2
    assert "sync_prospect_emails_sent(prospect.name)" in api
    assert "sync_prospect_emails_sent(prospect_name)" in api


def test_migration_backfills_existing_counts():
    setup = (APP / "setup" / "__init__.py").read_text()
    assert "ensure_prospect_emails_sent_sync()" in setup
    assert "sync_all_prospect_emails_sent()" in setup
