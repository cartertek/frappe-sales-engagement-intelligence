# CRM Conversion API

Methods:

- `preview_crm_conversion(prospect)`
- `find_crm_duplicates(prospect)`
- `create_crm_lead(prospect, options=None)` manager-only
- `create_or_link_crm_organization(prospect, options=None)` manager-only
- `create_or_link_contact(prospect, options=None)` manager-only
- `create_crm_deal(prospect, options=None)` manager-only and commercially guarded
- `link_existing_crm_record(prospect, doctype, record_name)` manager-only
- `sync_sei_context_to_crm(prospect)` manager-only

CRM actions delegate to M4 services. They are explicit, duplicate-aware, permission-gated, and blocked for Rejected / Do Not Contact prospects. Contact creation/linking uses Frappe's standalone `Contact` DocType. No endpoint creates ERPNext Lead / Opportunity / Quotation / Customer records.
