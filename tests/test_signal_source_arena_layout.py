import json
from pathlib import Path

SIGNAL_SCHEMA = Path(
    "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/sei_signal/sei_signal.json"
)


def test_signal_source_arena_is_in_overview_after_signal_type():
    schema = json.loads(SIGNAL_SCHEMA.read_text())
    order = schema["field_order"]

    assert order.index("source_arena") == order.index("signal_type") + 1
    assert order.index("signal_strength") == order.index("source_arena") + 1
    assert order.index("source_arena") < order.index("signal_type_definition_section")
