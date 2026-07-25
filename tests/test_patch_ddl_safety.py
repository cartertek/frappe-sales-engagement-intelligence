import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCH_ROOT = ROOT / "sales_engagement_intelligence" / "patches"

RAW_DDL_VIA_SQL = re.compile(
    r"frappe\.db\.sql\(\s*(?:f|r|fr|rf)?[\"'](?:\\n|\s)*(?:ALTER|CREATE\s+TABLE|DROP\s+TABLE|TRUNCATE)\b",
    re.IGNORECASE,
)


def test_patches_do_not_execute_ddl_through_db_sql():
    violations = []
    for path in PATCH_ROOT.rglob("*.py"):
        source = path.read_text()
        if RAW_DDL_VIA_SQL.search(source):
            violations.append(str(path.relative_to(ROOT)))

    assert not violations, (
        "Patch DDL must use frappe.db.sql_ddl or a Frappe schema API, not frappe.db.sql; "
        "raw DDL through db.sql is rejected during patch execution because it can implicitly commit: "
        + ", ".join(violations)
    )
