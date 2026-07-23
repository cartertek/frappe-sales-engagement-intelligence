from pathlib import Path

SCRIPT = (
    Path("sales_engagement_intelligence")
    / "sales_engagement_and_intelligence"
    / "doctype"
    / "sei_prospect"
    / "sei_prospect.js"
).read_text()


def test_saved_name_only_recipient_is_canonicalized_against_contact_options():
    assert "canonical_message_draft_recipient(row.to_contact, available)" in SCRIPT
    assert "row.to_contact = canonical" in SCRIPT
    assert "matches.length === 1 ? matches[0] : selected" in SCRIPT


def test_recipient_options_are_deduplicated_after_canonicalization():
    canonical_index = SCRIPT.index("canonical_message_draft_recipient(row.to_contact, available)")
    dedupe_index = SCRIPT.index("new Set([...available, ...saved])")
    assert canonical_index < dedupe_index
