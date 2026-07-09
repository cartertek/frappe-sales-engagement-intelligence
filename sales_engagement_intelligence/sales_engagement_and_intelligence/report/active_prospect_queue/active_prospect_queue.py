from __future__ import annotations

from sales_engagement_intelligence.sales_engagement_and_intelligence.reporting.reports import execute_report


def execute(filters=None):
    return execute_report('Active Prospect Queue', filters)
