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


_SEI_DOCTYPE_MODULE = "sales_engagement_intelligence.sales_engagement_and_intelligence.doctype"

override_doctype_class = {
    "SEI Prospect": f"{_SEI_DOCTYPE_MODULE}.prospect.prospect.SEIProspect",
    "SEI Signal": f"{_SEI_DOCTYPE_MODULE}.signal.signal.SEISignal",
    "SEI Thesis": f"{_SEI_DOCTYPE_MODULE}.thesis.thesis.SEIThesis",
    "SEI Asset": f"{_SEI_DOCTYPE_MODULE}.asset.asset.SEIAsset",
    "SEI Interaction Attribution": (
        f"{_SEI_DOCTYPE_MODULE}.interaction_attribution."
        "interaction_attribution.SEIInteractionAttribution"
    ),
}



app_include_css = "/assets/sales_engagement_intelligence/css/desktop.css"
app_include_js = "/assets/sales_engagement_intelligence/js/desktop_icons.js"

after_migrate = "sales_engagement_intelligence.setup.desktop_layout.after_migrate"
