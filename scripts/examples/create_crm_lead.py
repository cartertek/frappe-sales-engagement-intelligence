import os

from _client import call

call(
    "sales_engagement_intelligence.sales_engagement_and_intelligence.api.create_crm_lead",
    prospect=os.environ["SEI_PROSPECT"],
    options={"allow_duplicate": False},
)
