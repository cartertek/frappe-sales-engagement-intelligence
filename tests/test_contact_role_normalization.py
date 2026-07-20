from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "sales_engagement_intelligence" / "patches" / "v0_0_1" / "seed_playbooks_and_templates.py"
REPLACE = ROOT / "sales_engagement_intelligence" / "patches" / "v0_0_1" / "replace_theses_with_playbooks.py"
CONTROLLER = (
    ROOT
    / "sales_engagement_intelligence"
    / "sales_engagement_and_intelligence"
    / "doctype"
    / "sei_contact_role"
    / "sei_contact_role.py"
)


def test_seeded_contact_roles_are_single_roles_without_slashes():
    text = SEED.read_text() + REPLACE.read_text()
    assert "Founder / Operator" not in text
    assert "founder/operator" not in text
    assert "Innovation / AI Lead" not in text


def test_seeded_contact_roles_use_canonical_capitalization():
    text = SEED.read_text()
    for noncanonical in (
        "operations lead",
        "delivery lead",
        "account lead",
        "engineering manager",
        "product lead",
        "technical lead",
        "Agency owner",
        "MSP owner",
    ):
        assert noncanonical not in text


def test_contact_role_validation_rejects_slash_delimited_names():
    text = CONTROLLER.read_text()
    assert 'if "/" in (self.role_name or "")' in text
    assert "cannot contain a slash" in text
