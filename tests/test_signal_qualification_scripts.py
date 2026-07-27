import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "sales_engagement_intelligence"
DOCTYPE = APP / "sales_engagement_and_intelligence" / "doctype"
QUALIFICATION = APP / "sales_engagement_and_intelligence" / "services" / "qualification.py"
RUNNER = APP / "sales_engagement_and_intelligence" / "services" / "signal_qualification_script.py"
PATCHES = APP / "patches.txt"


def test_playbook_has_javascript_qualification_script_and_no_signal_rules_field():
    data = json.loads((DOCTYPE / "sei_playbook" / "sei_playbook.json").read_text())
    fields = {field["fieldname"]: field for field in data["fields"]}
    assert "signal_rules" not in fields
    script = fields["signal_qualification_script"]
    assert script["fieldtype"] == "Code"
    assert script["options"] == "JavaScript"
    assert "signal_qualification_script" in data["field_order"]
    assert data["field_order"].index("signal_qualification_script") < data["field_order"].index(
        "qualification_guidance_section"
    )


def test_legacy_signal_rule_doctype_is_removed():
    assert not (DOCTYPE / "sei_playbook_signal_rule").exists()


def test_qualification_groups_eligible_observed_signals_by_signal_type_playbook():
    source = QUALIFICATION.read_text()
    assert '"evidence_basis": "Observed"' in source
    assert '"exclude_from_qualification": 0' in source
    assert 'fields=["name", "playbook"]' in source
    assert 'grouped[playbook].append(signal)' in source
    assert 'evaluate_signal_qualification_script(' in source
    assert 'if precedence[group_status] > precedence[aggregate_status]:' in source
    assert 'group_status in ("Qualified", "Needs Review", "Manually Approved")' in source
    assert 'status = script_status' in source


def test_runner_constrains_node_vm_and_exposes_only_signal_data():
    source = RUNNER.read_text()
    assert "vm.createContext" in source
    assert "codeGeneration: { strings: false, wasm: false }" in source
    assert "sandbox.signals" in source
    assert "--max-old-space-size=32" in source
    assert "timeout=5.0" in source
    assert "sandbox.QualificationStatus = QualificationStatus" in source
    assert "Qualification script must return a QualificationStatus value." in source


def test_default_script_preserves_previous_threshold():
    source = RUNNER.read_text()
    assert 'strength == \\"Strong\\"' in source
    assert 'strength == \\"Moderate\\"' in source
    assert ".length > 1" in source
    assert "QualificationStatus.NeedsReview" in source


def test_playbook_schema_supplies_default_qualification_script_and_backfill_migration():
    data = json.loads((DOCTYPE / "sei_playbook" / "sei_playbook.json").read_text())
    fields = {field["fieldname"]: field for field in data["fields"]}
    default = fields["signal_qualification_script"]["default"]
    assert "QualificationStatus.Qualified" in default
    assert "QualificationStatus.NeedsReview" in default
    assert "QualificationStatus.Unqualified" in default
    legacy_migration_entry = (
        "sales_engagement_intelligence.patches.v0_0_1."
        "replace_playbook_signal_rules_with_qualification_scripts"
    )
    backfill_migration_entry = (
        "sales_engagement_intelligence.patches.v0_0_1."
        "backfill_default_playbook_qualification_script"
    )
    patch_lines = PATCHES.read_text().splitlines()
    assert legacy_migration_entry not in patch_lines
    assert backfill_migration_entry in patch_lines
    assert (
        "sales_engagement_intelligence.patches.v0_0_1."
        "upgrade_default_playbook_qualification_script_enum"
    ) in patch_lines
    assert not (
        APP / "patches" / "v0_0_1" / "replace_playbook_signal_rules_with_qualification_scripts.py"
    ).exists()

    backfill = (
        APP / "patches" / "v0_0_1" / "backfill_default_playbook_qualification_script.py"
    ).read_text()
    assert "UPDATE `tabSEI Playbook`" in backfill
    assert "signal_qualification_script IS NULL" in backfill
    assert "TRIM(signal_qualification_script) = ''" in backfill


def test_playbook_script_changes_recalculate_affected_prospects():
    controller = (DOCTYPE / "sei_playbook" / "sei_playbook.py").read_text()
    source = QUALIFICATION.read_text()
    assert 'has_value_changed("signal_qualification_script")' in controller
    assert "recalculate_prospects_for_playbook" in controller
    assert 'filters={"playbook": playbook}' in source
    assert 'filters={"signal_type": ["in", signal_types]}' in source


def test_legacy_disqualifier_check_feature_is_removed():
    signal = json.loads(
        (DOCTYPE / "sei_signal" / "sei_signal.json").read_text()
    )
    fields = {field["fieldname"] for field in signal["fields"]}
    assert "disqualifier_checks" not in fields
    assert "is_strength_capped" not in fields
    assert not (DOCTYPE / "sei_signal_disqualifier_check").exists()

    signal_py = (DOCTYPE / "sei_signal" / "sei_signal.py").read_text()
    signal_js = (DOCTYPE / "sei_signal" / "sei_signal.js").read_text()
    qualification = (APP / "sales_engagement_and_intelligence" / "services" / "qualification.py").read_text()
    assert "has_applied_disqualifier" not in signal_py
    assert "disqualifier_checks" not in signal_js
    assert "is_strength_capped" not in qualification


def test_disqualifier_cleanup_patch_uses_ddl_api_for_schema_changes():
    patch = (
        APP / "patches" / "v0_0_1" / "remove_signal_disqualifier_checks.py"
    ).read_text()
    assert 'frappe.db.sql_ddl("ALTER TABLE `tabSEI Signal` DROP COLUMN `is_strength_capped`")' in patch
    assert 'frappe.db.sql("ALTER TABLE' not in patch
