"""Repair Milestone 2 data-model namespace drift without touching Desk navigation."""

from __future__ import annotations

import frappe

from sales_engagement_intelligence.patches.v0_0_1.add_milestone_2_crm_custom_fields import (
    execute as create_milestone_2_crm_custom_fields,
)

APP_MODULE = "Sales Engagement and Intelligence"

DOCTYPE_RENAMES = {
    "Prospect": "SEI Prospect",
    "Signal": "SEI Signal",
    "Thesis": "SEI Thesis",
    "Marketing Asset": "SEI Asset",
    "Interaction Attribution": "SEI Interaction Attribution",
}

OLD_ENGAGEMENT_CUSTOM_FIELDS = (
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
)


def execute():
    repair_erpnext_asset_doctype()
    repair_app_owned_doctypes()
    remove_old_engagement_custom_fields()
    create_milestone_2_crm_custom_fields()


def repair_erpnext_asset_doctype():
    if frappe.db.exists("DocType", "Asset"):
        module = frappe.db.get_value("DocType", "Asset", "module")
        if module == APP_MODULE:
            frappe.reload_doc("assets", "doctype", "asset", force=True)


def repair_app_owned_doctypes():
    for old_name, new_name in DOCTYPE_RENAMES.items():
        if not frappe.db.exists("DocType", old_name):
            continue
        if frappe.db.get_value("DocType", old_name, "module") != APP_MODULE:
            continue
        if frappe.db.exists("DocType", new_name):
            # Do not delete or merge data here. Production does not have app-owned
            # unprefixed DocTypes; this guard prevents collisions on repaired sites.
            continue
        frappe.rename_doc("DocType", old_name, new_name, force=True)


def remove_old_engagement_custom_fields():
    for custom_field in OLD_ENGAGEMENT_CUSTOM_FIELDS:
        if frappe.db.exists("Custom Field", custom_field):
            frappe.delete_doc("Custom Field", custom_field, ignore_permissions=True, force=True)
