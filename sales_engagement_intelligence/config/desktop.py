from frappe import _


def get_data():
    return [
        {
            "module_name": "Sales Engagement and Intelligence",
            "category": "Modules",
            "label": _("Sales Engagement and Intelligence"),
            "color": "grey",
            "icon": "octicon octicon-broadcast",
            "type": "module",
            "description": _("Pre-CRM outreach intelligence and sales engagement workspace."),
        }
    ]
