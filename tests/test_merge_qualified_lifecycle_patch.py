from pathlib import Path


def test_patch_migrates_only_lifecycle_qualified_records():
    source = Path(
        "sales_engagement_intelligence/patches/v0_0_1/merge_qualified_lifecycle_into_research_complete.py"
    ).read_text()
    assert '{"lifecycle_status": "Qualified"}' in source
    assert '"Research Complete"' in source
    assert '"qualification_status"' not in source


def test_patch_is_registered():
    patches = Path("sales_engagement_intelligence/patches.txt").read_text()
    assert "merge_qualified_lifecycle_into_research_complete" in patches
