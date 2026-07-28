from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCH = ROOT / (
    "sales_engagement_intelligence/patches/v0_0_1/"
    "migrate_observed_facts_to_child_table.py"
)
PATCHES = ROOT / "sales_engagement_intelligence/patches.txt"


def test_patch_migrates_legacy_value_into_child_row_idempotently():
    source = PATCH.read_text()

    assert 'has_column("SEI Signal", "observed_fact")' in source
    assert '"SEI Signal Observed Fact"' in source
    assert '"parentfield": "observed_facts"' in source
    assert "if exists:" in source


def test_patch_is_registered():
    assert (
        "sales_engagement_intelligence.patches.v0_0_1."
        "migrate_observed_facts_to_child_table"
    ) in PATCHES.read_text()
