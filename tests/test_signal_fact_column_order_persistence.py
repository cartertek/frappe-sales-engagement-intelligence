import json
from pathlib import Path

ROOT = Path("sales_engagement_intelligence/sales_engagement_and_intelligence")
SCHEMA = json.loads(
    (ROOT / "doctype/sei_signal_observed_fact/sei_signal_observed_fact.json").read_text()
)
PATCH = Path(
    "sales_engagement_intelligence/patches/v0_0_1/restore_signal_fact_column_order.py"
).read_text()

EXPECTED = [
    "fact",
    "source_url",
    "source_date",
    "evidence_basis",
    "evidence_specificity",
]


def test_fact_schema_persists_intended_column_order():
    assert SCHEMA["field_order"] == EXPECTED
    assert [field["fieldname"] for field in SCHEMA["fields"]] == EXPECTED
    assert [field["idx"] for field in SCHEMA["fields"]] == [1, 2, 3, 4, 5]


def test_new_patch_restores_database_docfield_order_after_schema_sync():
    for fieldname in EXPECTED:
        assert f'"{fieldname}"' in PATCH
    assert 'frappe.clear_cache(doctype=parent)' in PATCH
