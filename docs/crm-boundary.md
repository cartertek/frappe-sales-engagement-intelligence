# CRM Architecture Boundary

Sales Engagement and Intelligence is the pre-CRM outreach intelligence layer.

Frappe CRM is the primary sales-engagement CRM layer. ERPNext is the downstream ERP/accounting layer.

## Target Architecture

```text
Sales Engagement and Intelligence
→ pre-CRM outreach intelligence and qualification
→ Frappe CRM Lead / Deal
→ ERPNext Quotation / Customer / accounting
```

## Responsibility Split

Frappe CRM owns qualified leads, deals, lead/deal pipeline views, tasks, notes, call logs, email templates, assignments, and sales engagement activity.

ERPNext owns quotations, customers, items/products if needed, sales orders if needed, invoices, accounting, and downstream business records.

Sales Engagement and Intelligence owns pre-CRM research, signal evidence, qualification, thesis alignment, analytics, and conversion into Frappe CRM Leads.

ERPNext Lead and ERPNext Opportunity are not the primary conversion targets for this implementation.

## Boundary Rules

Unqualified or half-researched companies should not immediately become Frappe CRM Leads.

They should first live in the future custom Outreach Prospect DocType.
Conversion into Frappe CRM should happen only after qualification criteria are met.

Formal quoting, customer creation, invoicing, and accounting should flow downstream into ERPNext.
