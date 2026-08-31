import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_ROOT = ROOT / "sales_engagement_intelligence" / "sales_engagement_and_intelligence" / "report"
WORKSPACE = (
    ROOT
    / "sales_engagement_intelligence"
    / "sales_engagement_and_intelligence"
    / "workspace"
    / "engagement_reports"
    / "engagement_reports.json"
)


def test_engagement_workspace_report_links_resolve_to_shipped_reports():
    report_names = set()
    for path in REPORT_ROOT.glob("*/*.json"):
        payload = json.loads(path.read_text())
        report_name = payload.get("report_name")
        if report_name:
            report_names.add(report_name)

    workspace = json.loads(WORKSPACE.read_text())
    linked_reports = {
        row.get("link_to")
        for row in workspace.get("links", [])
        if row.get("type") == "Report" and row.get("link_to")
    }
    linked_reports.update(
        row.get("link_to")
        for row in workspace.get("shortcuts", [])
        if row.get("type") == "Report" and row.get("link_to")
    )

    missing = sorted(linked_reports - report_names)
    assert not missing, f"Workspace links to missing reports: {missing}"
