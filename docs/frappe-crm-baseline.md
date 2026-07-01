# Frappe CRM Baseline

Milestone 1 uses the standalone `crm` app on the same site as ERPNext and this app.

## Installed Apps Observed

Observed on `frappe.localhost`:

```text
frappe                        17.0.0-dev UNVERSIONED
erpnext                       17.0.0-dev UNVERSIONED
hrms                          17.0.0-dev UNVERSIONED
sales_engagement_intelligence 0.0.1      UNVERSIONED
crm                           2.0.0-dev  UNVERSIONED
```

## Coexistence Checks

- ERPNext desk loads.
- Frappe CRM interface loads.
- Existing ERPNext data remains intact.
- No migration or routing errors are obvious.
- Administrator can access both apps.
- The standalone Frappe CRM app and ERPNext CRM DocTypes both exist on the site, so Milestone 2 must explicitly target the standalone Frappe CRM DocTypes in module `FCRM`.

## Milestone 2 CRM Targets

Use these standalone Frappe CRM DocTypes as the integration targets:

| Concept | Target DocType | Module | Notes |
| --- | --- | --- | --- |
| Lead | `CRM Lead` | `FCRM` | Primary conversion target from SEI qualification. Required fields observed: `first_name`, `status`. |
| Deal | `CRM Deal` | `FCRM` | Qualified sales opportunity target after/alongside lead conversion. Required field observed: `status`. |
| Organization | `CRM Organization` | `FCRM` | Company/account-like object. `CRM Deal.organization` links here. |
| Contact row | `CRM Contacts` | `FCRM` | Child table used by `CRM Deal.contacts`; links to Frappe `Contact`. |
| Note | `FCRM Note` | `FCRM` | Uses `reference_doctype` / `reference_docname` dynamic link. |
| Task | `CRM Task` | `FCRM` | Uses `reference_doctype` / `reference_docname`; has `assigned_to`, `status`, `due_date`. |
| Call log | `CRM Call Log` | `FCRM` | Uses `reference_doctype` / `reference_docname`; can link to `FCRM Note`. |
| Lead source | `CRM Lead Source` | `FCRM` | Lookup table for lead/deal source. |
| Lead status | `CRM Lead Status` | `FCRM` | Lookup table for `CRM Lead.status`. |
| Deal status | `CRM Deal Status` | `FCRM` | Lookup table for `CRM Deal.status`. |

Do **not** use ERPNext CRM `Lead` / `Opportunity` as the primary M2 targets. Those DocTypes still exist under ERPNext CRM, but the selected architecture targets standalone Frappe CRM.

## Key Field Snapshot

### CRM Lead

Important observed fields:

- Person/contact fields: `salutation`, `first_name`, `last_name`, `lead_name`, `email`, `mobile_no`, `phone`, `gender`, `job_title`.
- Organization fields: `organization` (Data), `website`, `territory`, `industry`, `no_of_employees`, `annual_revenue`.
- CRM routing fields: `source` (`CRM Lead Source`), `lead_owner` (`User`), `status` (`CRM Lead Status`), `converted`.
- Products: `products` child table (`CRM Products`), `total`, `net_total`.
- SLA/activity metadata: `sla`, `sla_status`, `communication_status`, response timing fields, `status_change_log`.
- Lost state: `lost_reason`, `lost_notes`.

Minimum creation implication for M2: `first_name` and `status` are required.

### CRM Deal

Important observed fields:

- Organization/sales fields: `organization` (`CRM Organization`), `status` (`CRM Deal Status`), `deal_owner`, `next_step`, `probability`, `expected_deal_value`, `deal_value`, `expected_closure_date`, `closed_date`.
- Contact fields: `contacts` child table (`CRM Contacts`), `contact` (`Contact`).
- Lead linkage: `lead` (`CRM Lead`), `source` (`CRM Lead Source`), `lead_name`.
- Denormalized organization/person detail fields: `organization_name`, `website`, `no_of_employees`, `job_title`, `territory`, `currency`, `annual_revenue`, `industry`, `first_name`, `last_name`, `email`, `mobile_no`, `phone`.
- Products: `products` child table (`CRM Products`), `total`, `net_total`.
- ERPNext integration custom field, when enabled by `ERPNext CRM Settings`: `erpnext_customer`.

Minimum creation implication for M2: `status` is required. `organization`, `lead`, and contacts are optional at the schema level but important for useful downstream records.

### CRM Organization

Important observed fields:

- `organization_name`, `website`, `territory`, `industry`, `no_of_employees`, `annual_revenue`, `currency`, `exchange_rate`, `organization_logo`, `address`.

### Notes, Tasks, and Calls

`FCRM Note`, `CRM Task`, and `CRM Call Log` all support generic linking through `reference_doctype` and `reference_docname`. This is the expected path for attaching SEI-generated context or follow-up activity to a CRM Lead or CRM Deal after conversion.

## ERPNext Integration Baseline

Frappe CRM provides a Single DocType named `ERPNext CRM Settings`.

Observed fields include:

- `enabled`
- `erpnext_company`
- `is_erpnext_in_different_site`
- `erpnext_site_url`
- `api_key`
- `api_secret`
- `create_customer_on_status_change`
- `deal_status`
- `sync_issues`

No `ERPNext CRM Settings` values are currently configured in `tabSingles` on the live site.

When enabled for same-site ERPNext, the integration code:

- Adds Quotation link filtering so `Quotation.quotation_to` can include `CRM Deal`.
- Adds custom fields:
  - `CRM Deal.erpnext_customer`
  - `Quotation.crm_deal`
  - `Customer.crm_deal`
  - `CRM Product.erpnext_item_code`
  - `Item.crm_product_code` when ERPNext Item exists.
- Creates a CRM Form Script named `Create Quotation from CRM Deal`.
- Adds a “Create Quotation” action to the CRM Deal form script.
- Can auto-create a Customer when a CRM Deal reaches the configured `deal_status`, if `create_customer_on_status_change` is enabled.
- Can create/fetch the Customer behind a CRM Deal when a Sales Order is opened from a CRM Deal Quotation.

Same-site quotation path observed in code:

```text
CRM Deal
→ Create Quotation action
→ /app/quotation/new?quotation_to=CRM Deal&crm_deal=<deal>&party_name=<deal>&company=<erpnext_company>...
```

If a Customer already exists or has been created for the CRM Deal, the quotation path uses:

```text
quotation_to=Customer
party_name=<customer>
crm_deal=<deal>
```

Remote-site ERPNext mode exists, but is not the current intended architecture because ERPNext is installed on the same site.

## Milestone 2 Notes

Before implementing conversion logic, M2 should decide:

- Default `CRM Lead Status` for newly converted SEI prospects.
- Default `CRM Deal Status` if SEI can create deals directly.
- Whether SEI conversion creates only `CRM Lead`, or can optionally create `CRM Organization` / `CRM Deal`.
- Whether SEI context should attach to CRM records as `FCRM Note`, `CRM Task`, or both.
- Whether and when to enable `ERPNext CRM Settings`; enabling it creates custom fields and form scripts.
