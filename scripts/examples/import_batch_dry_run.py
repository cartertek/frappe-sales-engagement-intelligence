import os

from _client import call

call(
    "sales_engagement_intelligence.sales_engagement_and_intelligence.api.dry_run_import",
    batch=os.environ["SEI_IMPORT_BATCH"],
)
