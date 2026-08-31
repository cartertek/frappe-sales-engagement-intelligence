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


def test_engagement_reports_workspace_links_to_existing_reports():
    report_names = set()
    for path in REPORT_ROOT.glob("*/*.json"):
        data = json.loads(path.read_text())
        if data.get("report_name"):
            report_names.add(data["report_name"])

    workspace = json.loads(WORKSPACE.read_text())
    links = {
        row.get("link_to")
        for key in ("links", "shortcuts")
        for row in workspace.get(key, [])
        if row.get("type") == "Report" and row.get("link_to")
    }
    missing = sorted(links - report_names)
    assert not missing, f"Workspace links to missing reports: {missing}"
