# ERPNext CRM Boundary

ERPNext remains the CRM system of record. Sales Engagement and Intelligence is the pre-CRM intelligence layer.

## Native ERPNext Objects

The custom app should integrate with, not replace, these ERPNext objects:

- Lead
- Contact
- Opportunity
- Campaign
- Communication
- ToDo
- Quotation
- Customer

## Boundary Rules

Use ERPNext `Lead` for a prospect that is qualified, contactable, and worth entering into formal CRM tracking.

Use ERPNext `Contact` for a known person at the company or intermediary organization.

Use ERPNext `Opportunity` for a prospect that has shown commercial interest, booked a meeting, discussed a paid diagnostic, or otherwise entered a realistic sales conversation.

Use ERPNext `Communication` for email or message history where appropriate.

Use ERPNext `ToDo` for follow-up reminders when the custom app chooses to create native ERPNext reminders.

Use ERPNext `Campaign` for broad source, campaign, or arena grouping if useful.

Use ERPNext `Quotation` for formal proposals or quotes after the sales process has advanced.

Use ERPNext `Customer` for won clients.

## Explicit Boundary

Unqualified or half-researched companies should not become ERPNext Leads merely because they were discovered.

They should first live in the future custom `Outreach Prospect` DocType. Conversion into native CRM records should happen only after qualification criteria are met and a deliberate conversion action is taken.
