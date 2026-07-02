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
                    "Assets",
                    "CRM Conversion",
                    "Reports",
                    "Settings",
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
                    "CRM Lead-engagement_intelligence_section",
                    "CRM Lead-engagement_prospect",
                    "CRM Lead-engagement_source_arena",
                    "CRM Lead-engagement_thesis",
                    "CRM Lead-engagement_qualification_summary",
                    "CRM Deal-engagement_intelligence_section",
                    "CRM Deal-engagement_prospect",
                    "CRM Deal-engagement_source_arena",
                    "CRM Deal-engagement_thesis",
                    "CRM Deal-engagement_primary_signal",
                ],
            ],
        ],
    },
]


app_include_css = "/assets/sales_engagement_intelligence/css/desktop.css"
app_include_js = "/assets/sales_engagement_intelligence/js/desktop_icons.js"

after_migrate = [
    "sales_engagement_intelligence.setup.desktop_layout.after_migrate",
    "sales_engagement_intelligence.setup.desktop.after_migrate",
    "sales_engagement_intelligence.patches.v0_0_1.seed_theses.execute",
]
