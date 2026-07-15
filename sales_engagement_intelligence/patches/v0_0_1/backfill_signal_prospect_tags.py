from __future__ import annotations


def execute() -> None:
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.prospect_tag_sync import (
        ensure_signal_prospect_tag_trigger,
        sync_all_signal_prospect_tags,
    )

    sync_all_signal_prospect_tags()
    ensure_signal_prospect_tag_trigger()
