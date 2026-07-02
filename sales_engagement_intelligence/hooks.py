app_name = "sales_engagement_intelligence"
app_title = "Sales Engagement and Intelligence"
app_publisher = "Cartertek LLC"
app_description = "Pre-CRM outreach intelligence layer for Frappe CRM and ERPNext."
app_email = "admin@cartertek.ai"
app_license = "MIT"

add_to_apps_screen = [
    {
        "name": "sales_engagement_intelligence",
        "logo": "/assets/sales_engagement_intelligence/desktop_icons/app.svg",
        "title": "Sales Engagement and Intelligence",
        "route": "/app/sales-engagement-and-intelligence",
    }
]

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
            [
                "name",
                "in",
                [
                    "Sales Engagement and Intelligence",
                    "Prospecting",
                    "Signals",
                    "Touchpoints",
                    "Theses and Assets",
                    "CRM Attribution",
                    "Engagement Reports",
                    "Engagement Settings",
                ],
            ],
        ],
    },
    {
        "dt": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                [
                    "CRM Lead-sei_section",
                    "CRM Lead-sei_prospect",
                    "CRM Lead-sei_source_arena",
                    "CRM Lead-sei_thesis",
                    "CRM Lead-sei_qualification_summary",
                    "CRM Deal-sei_section",
                    "CRM Deal-sei_prospect",
                    "CRM Deal-sei_source_arena",
                    "CRM Deal-sei_thesis",
                    "CRM Deal-sei_primary_signal",
                ],
            ],
        ],
    },
]


after_migrate = [
    "sales_engagement_intelligence.patches.v0_0_1.seed_theses.execute",
]
