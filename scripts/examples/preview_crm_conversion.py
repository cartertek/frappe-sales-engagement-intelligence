import os

from _client import call

call(
    "sales_engagement_intelligence.sales_engagement_and_intelligence.api.preview_crm_conversion",
    prospect=os.environ["SEI_PROSPECT"],
)
