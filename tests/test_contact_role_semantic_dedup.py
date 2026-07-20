from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = (
    ROOT / "sales_engagement_intelligence" / "patches" / "v0_0_1"
    / "seed_playbooks_and_templates.py"
).read_text()
CLEANUP = (
    ROOT / "sales_engagement_intelligence" / "sales_engagement_and_intelligence"
    / "services" / "contact_role_cleanup.py"
).read_text()


def test_obsolete_semantic_roles_are_not_seeded():
    assert "Operations Owner" not in SEED
    assert "Engineering Lead" not in SEED


def test_cleanup_merges_obsolete_semantic_roles():
    assert '("Operations Owner", "Operations Lead")' in CLEANUP
    assert '("Engineering Lead", "Technical Lead")' in CLEANUP
    assert "merge=True" in CLEANUP
