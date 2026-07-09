from _client import call

call(
    "sales_engagement_intelligence.sales_engagement_and_intelligence.api.create_prospect",
    payload={
        "prospect_name": "Example Co",
        "website": "https://example.com",
        "source_arena": "Agency Directory",
        "source_url": "https://example.com/profile",
        "offer": "Project rescue",
        "next_action": "Research technical fit",
    },
)
