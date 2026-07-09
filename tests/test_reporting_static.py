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
