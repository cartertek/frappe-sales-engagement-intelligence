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


def test_removed_quick_filter_fields_remain_available_as_regular_filters():
    schema = json.loads(PROSPECT_SCHEMA.read_text())
    fields = {field["fieldname"]: field for field in schema["fields"]}

    removed_quick_filters = {
        "website",
        "prospect_type",
        "signals",
        "qualification_status",
        "crm_lead",
        "crm_deal",
    }

    for fieldname in removed_quick_filters:
        assert fieldname in fields
        assert fields[fieldname]["fieldtype"] not in {
            "Section Break",
            "Column Break",
            "Tab Break",
            "HTML",
            "Table",
        }
        assert not fields[fieldname].get("in_standard_filter")
