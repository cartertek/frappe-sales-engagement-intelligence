app_name = "sales_engagement_intelligence"
app_title = "Sales Engagement and Intelligence"
app_publisher = "Cartertek LLC"
app_description = "Pre-CRM outreach intelligence layer for Frappe CRM and ERPNext."
app_email = "admin@cartertek.ai"
app_license = "MIT"
required_apps = ["frappe/erpnext"]
source_link = "https://github.com/cartertek/frappe-sales-engagement-intelligence"
app_logo_url = "/assets/sales_engagement_intelligence/desktop_icons/app.svg"
app_home = "/desk/prospecting"

add_to_apps_screen = [
    {
        "name": "sales_engagement_intelligence",
        "logo": app_logo_url,
        "title": "Sales Engagement and Intelligence",
        "route": app_home,
        "has_permission": (
            "sales_engagement_intelligence.sales_engagement_and_intelligence"
            ".utils.check_app_permission"
        ),
    }
]

# The Milestone 1 foundation intentionally avoids scheduled jobs, email senders,
# outbound automation, and any background process that could send outreach.


# Includes in <head>
# ------------------
app_include_js = [
    "sales_engagement_intelligence.bundle.js",
]
app_include_css = "sales_engagement_intelligence.bundle.css"


# Installation / app lifecycle
after_install = "sales_engagement_intelligence.install.after_install"
after_migrate = "sales_engagement_intelligence.setup.after_migrate"
after_app_install = "sales_engagement_intelligence.setup.after_app_install"
before_app_uninstall = "sales_engagement_intelligence.setup.before_app_uninstall"
before_uninstall = "sales_engagement_intelligence.uninstall.before_uninstall"

fixtures = [
    {
        "dt": "Role",
        "filters": [["name", "in", ["Sales Engagement Manager", "Sales Engagement User"]]],
    },
    {
        "dt": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                [
                    "CRM Lead-sei_tab",
                    "CRM Lead-sei_section",
                    "CRM Lead-sei_prospect",
                    "CRM Lead-sei_source_arena",
                    "CRM Lead-sei_thesis",
                    "CRM Lead-sei_qualification_summary",
                    "CRM Deal-sei_tab",
                    "CRM Deal-sei_section",
                    "CRM Deal-sei_prospect",
                    "CRM Deal-sei_source_arena",
                    "CRM Deal-sei_thesis",
                    "CRM Deal-sei_primary_signal",
                ],
            ]
        ],
    },
]
