from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCH = ROOT / "sales_engagement_intelligence/patches/v0_0_1/backfill_signal_names.py"
PATCHES = ROOT / "sales_engagement_intelligence/patches.txt"


def test_patch_backfills_only_blank_names_from_signal_type():
    source = PATCH.read_text()
    assert 'SET `signal_name` = `signal_type`' in source
    assert "TRIM(`signal_name`) = ''" in source
    assert "TRIM(`signal_type`) != ''" in source


def test_patch_is_registered():
    assert "sales_engagement_intelligence.patches.v0_0_1.backfill_signal_names" in PATCHES.read_text()
