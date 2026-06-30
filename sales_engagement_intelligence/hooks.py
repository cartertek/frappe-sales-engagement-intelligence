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

# Desktop launcher records are maintained after migrate because Frappe
# orphan cleanup deletes standard Desktop Icon / Workspace Sidebar resources
# that are not part of the core desktop registry.
after_migrate = "sales_engagement_intelligence.setup.desktop.after_migrate"
