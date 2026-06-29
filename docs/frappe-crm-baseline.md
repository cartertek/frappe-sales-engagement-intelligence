# Frappe CRM Baseline

Milestone 1 requires the standalone crm app on the same site as ERPNext and this app.

## Expected Apps

frappe, erpnext, hrms, crm, sales_engagement_intelligence

## Coexistence Checks

- ERPNext desk loads.
- Frappe CRM interface loads.
- Existing ERPNext data remains intact.
- No migration or routing errors are obvious.
- Administrator can access both apps.

## ERPNext Integration Baseline

- Document whether a Frappe CRM Deal can create or link to an ERPNext Quotation.
- Document whether a Frappe CRM Deal can create or link to an ERPNext Customer.
- Document how Frappe CRM contacts/organizations relate to ERPNext records.
- Document any setup required for the CRM to ERPNext path.

## Schema Discovery Checklist

Before Milestone 2, identify exact DocType names, fields, permissions, and extension points for:

- CRM Lead
- CRM Deal
- CRM Organization
- CRM Contact
- CRM Note
- CRM Task
- CRM Call Log
- CRM Email Template

Do not implement outreach DocTypes until this discovery is complete.
