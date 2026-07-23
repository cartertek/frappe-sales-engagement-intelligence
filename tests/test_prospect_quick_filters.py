from __future__ import annotations

import json
from pathlib import Path

PROSPECT_SCHEMA = Path(
    "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/"
    "sei_prospect/sei_prospect.json"
)


def test_prospect_quick_filters_are_limited_to_requested_fields():
    schema = json.loads(PROSPECT_SCHEMA.read_text())
    quick_filters = {
        field["fieldname"]
        for field in schema["fields"]
        if field.get("in_standard_filter")
    }

    assert quick_filters == {
        "prospect_name",
        "lifecycle_status",
        "normalized_domain",
        "arenas",
        "playbooks",
    }
