from pathlib import Path

SEED = Path(
    "sales_engagement_intelligence/patches/v0_0_1/seed_playbooks_and_templates.py"
).read_text()


def test_reactivation_seed_uses_canonical_contact_roles():
    assert "Original contact" not in SEED
    assert "new role owner" not in SEED
    assert '"Primary Contact, owner, Founder, CTO, operations lead"' in SEED


def test_founder_operator_role_uses_canonical_punctuation():
    assert '"founder/operator"' not in SEED
