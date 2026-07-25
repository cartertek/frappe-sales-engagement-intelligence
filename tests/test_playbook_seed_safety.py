from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SETUP = ROOT / "sales_engagement_intelligence/setup/__init__.py"
SEED = ROOT / "sales_engagement_intelligence/patches/v0_0_1/seed_playbooks_and_templates.py"


def test_after_migrate_does_not_overwrite_existing_seed_records():
    source = SETUP.read_text()
    assert "seed_playbooks_and_templates(update_existing=False)" in source


def test_seed_supports_create_missing_without_rewriting_existing_records():
    source = SEED.read_text()
    assert "def execute(*, update_existing: bool = True)" in source
    assert "if exists and not update_existing:" in source
    assert "if not update_existing:" in source
