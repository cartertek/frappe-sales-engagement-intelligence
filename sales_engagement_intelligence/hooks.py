app_name = "sales_engagement_intelligence"
app_title = "Sales Engagement and Intelligence"
app_publisher = "Cartertek LLC"
app_description = "Pre-CRM outreach intelligence layer for Frappe CRM and ERPNext."
app_email = "admin@cartertek.ai"
app_license = "MIT"

# The Milestone 1 foundation intentionally avoids scheduled jobs, email senders,
# outbound automation, and any background process that could send outreach.

fixtures = [
    {
        "dt": "Role",
        "filters": [
            [
                "role_name",
                "in",
                [
                    "Sales Engagement Manager",
                    "Sales Engagement User",
                ],
            ]
        ],
    },
    {
        "dt": "Workspace",
        "filters": [
            ["name", "=", "Sales Engagement and Intelligence"],
        ],
    },
]
