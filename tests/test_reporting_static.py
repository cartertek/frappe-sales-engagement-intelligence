from __future__ import annotations

import ast
import json
from pathlib import Path

REPORT_ROOT = Path("sales_engagement_intelligence/sales_engagement_and_intelligence/report")
REPORTING_MODULE = Path(
    "sales_engagement_intelligence/sales_engagement_and_intelligence/reporting/reports.py"
)
EXPECTED_REPORTS = {
    "Prospect Lifecycle Summary",
    "Active Prospect Queue",
    "Ready for CRM Conversion",
    "Terminal Status Review",
    "Signals by Type and Strength",
    "Qualification by Signal Type",
    "Inferred Signal Review",
    "Missing Evidence Report",
    "Prospects by Source Arena",
    "Outcomes by Thesis",
    "Asset Usage and Outcomes",
    "Offer Performance",
    "CRM Conversion Summary",
    "CRM Lead Conversion Detail",
    "CRM Deal Conversion Detail",
    "CRM Context Missing",
    "Possible Duplicate CRM Conversion Review",
    "Import Batch Summary",
    "Import Batch Row Errors",
    "Import Source Quality",
    "Data Hygiene Dashboard",
    "Interaction Attribution Summary",
    "Response Category by Thesis",
    "Channel Outcome Report",
}

MUTATION_TOKENS = (
    ".insert(",
    ".save(",
    ".delete(",
    ".submit(",
    ".cancel(",
    "db.set_value",
    "frappe.new_doc",
    "frappe.get_doc(",
    "run_import",
    "convert_to_crm",
    "sendmail",
)


def _report_jsons() -> list[Path]:
    return sorted(REPORT_ROOT.glob("*/*.json"))


def test_milestone_6_reports_are_registered_as_standard_script_reports():
    reports = [json.loads(path.read_text()) for path in _report_jsons()]
    names = {report["name"] for report in reports}

    assert EXPECTED_REPORTS <= names
    for report in reports:
        if report["name"] not in EXPECTED_REPORTS:
            continue
        assert report["report_type"] == "Script Report"
        assert report["is_standard"] == "Yes"
        assert report["module"] == "Sales Engagement and Intelligence"
        assert report["roles"]


def test_each_report_wrapper_delegates_to_shared_read_only_executor():
    for path in REPORT_ROOT.glob("*/*.py"):
        source = path.read_text()
        tree = ast.parse(source)
        functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
        assert [fn.name for fn in functions] == ["execute"]
        assert "execute_report(" in source


def test_shared_reporting_module_does_not_contain_mutation_operations():
    source = REPORTING_MODULE.read_text()
    for token in MUTATION_TOKENS:
        assert token not in source

FILTERED_REPORTS = {
    "Active Prospect Queue": {
        "lifecycle_status",
        "qualification_status",
        "assigned_to",
        "source_arena",
        "sei_thesis",
        "next_action_date",
    },
    "Ready for CRM Conversion": {"source_arena", "sei_thesis", "next_action_date"},
    "Signals by Type and Strength": {
        "signal_type",
        "signal_strength",
        "evidence_basis",
        "exclude_from_qualification",
    },
    "Import Batch Summary": {
        "source_type",
        "source_arena",
        "import_kind",
        "import_mode",
        "status",
    },
    "Interaction Attribution Summary": {
        "interaction_type",
        "channel",
        "response_category",
        "sei_thesis",
        "sei_asset",
    },
}


def _report_folder(report_name: str) -> Path:
    return REPORT_ROOT / report_name.lower().replace(" / ", "_").replace(" ", "_")


def test_filterable_reports_have_client_side_filter_definitions():
    for report_name, expected_fields in FILTERED_REPORTS.items():
        folder = _report_folder(report_name)
        source = (folder / f"{folder.name}.js").read_text()
        assert f'frappe.query_reports["{report_name}"]' in source
        assert "filters:" in source
        for fieldname in expected_fields:
            assert f'fieldname: "{fieldname}"' in source


def test_milestone_6_workspace_sync_hook_is_registered():
    setup_source = Path("sales_engagement_intelligence/setup/__init__.py").read_text()
    assert "ensure_milestone_6_workspace_reports()" in setup_source
    assert "def ensure_milestone_6_workspace_reports()" in setup_source
    assert "def validate_milestone_6_workspace_reports()" in setup_source
    for report_name in FILTERED_REPORTS:
        assert report_name in setup_source or report_name in REPORTING_MODULE.read_text()
