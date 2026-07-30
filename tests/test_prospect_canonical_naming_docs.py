from pathlib import Path

ROOT = Path("docs")
IDENTITY = (ROOT / "operator_workflow/identity-contact-research.md").read_text()
ASSISTANT = (ROOT / "assistant_workflows/create-prospect-and-signal.md").read_text()
IMPORTS = (ROOT / "import_templates/README.md").read_text()
API = (ROOT / "api/prospects.md").read_text()


def test_prospect_name_is_explicitly_organization_level_at_all_creation_entrypoints():
    for text in (IDENTITY, ASSISTANT, IMPORTS, API):
        assert "canonical" in text.lower()
        assert "organization" in text.lower()
        assert "prospect_name" in text


def test_identity_guide_rejects_product_qualified_prospect_names():
    assert "use `Microsoft`, not `Microsoft Foundry`" in IDENTITY
    assert "use `SAP`, not `SAP SuccessFactors - Latest People Profile`" in IDENTITY
    assert "use `National University`, not `National University - Student Information System`" in IDENTITY
    assert "Do not create separate Prospects for different products or initiatives" in IDENTITY
