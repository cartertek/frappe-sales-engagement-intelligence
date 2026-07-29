from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCH_ROOT = ROOT / "sales_engagement_intelligence" / "patches"
FORBIDDEN = (
    "recalculate_prospects_for_playbook",
    "apply_qualification_result",
    "calculate_prospect_qualification",
    "apply_lifecycle_status",
)


def test_migrations_do_not_recalculate_prospect_operational_state():
    offenders = []
    for path in PATCH_ROOT.rglob("*.py"):
        source = path.read_text()
        for symbol in FORBIDDEN:
            if symbol in source:
                offenders.append(f"{path.relative_to(ROOT)}: {symbol}")
    assert not offenders, "Operational recalculation is forbidden in migrations:\n" + "\n".join(offenders)
