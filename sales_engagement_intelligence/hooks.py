app_name = "sales_engagement_intelligence"
app_title = "Sales Engagement and Intelligence"
app_publisher = "Cartertek LLC"
app_description = "Pre-CRM outreach intelligence layer for Frappe CRM and ERPNext."
app_email = "admin@cartertek.ai"
app_license = "MIT"

add_to_apps_screen = [
    {
        "name": "sales_engagement_intelligence",
        "logo": "/assets/sales_engagement_intelligence/desktop_icons/sei_app.svg",
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
]


app_include_css = "/assets/sales_engagement_intelligence/css/sei_desktop.css"
