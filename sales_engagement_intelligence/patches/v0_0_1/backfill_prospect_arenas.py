from sales_engagement_intelligence.sales_engagement_and_intelligence.services import prospect_signal_type_sync


def execute():
    prospect_signal_type_sync.sync_all_prospect_signal_types()
