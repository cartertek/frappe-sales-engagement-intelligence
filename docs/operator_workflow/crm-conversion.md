# CRM Conversion

SEI prepares conversion context, but Frappe CRM owns the sales records. CRM handoff is explicit and user-controlled.

1. Confirm the prospect is Qualified or Manually Approved.
2. Confirm it is not Rejected and not Do Not Contact.
3. Confirm no CRM Lead has already been created.
4. Use **CRM Preparation → Mark Ready for CRM Conversion** to approve the CRM handoff. If a requirement is not met, the form displays a checklist showing which checks passed or failed.
5. If contact information exists, the lifecycle becomes Ready for CRM Conversion immediately.
6. If contact information is missing, the lifecycle becomes Find Contact. Adding contact information later automatically advances it to Ready for CRM Conversion.
7. Preview CRM conversion and review duplicate candidates.
8. Create or link CRM Lead, CRM Organization, Contact, and CRM Deal only with explicit action.
9. Create a CRM Deal only where there is a commercial basis or manager override.
10. Sync SEI context to CRM after linking or creation where needed.

A Qualified prospect remains Qualified until the user explicitly approves CRM handoff. Find Contact therefore means the handoff was approved but the required contact path is not yet available.

SEI never creates ERPNext Lead, Opportunity, Quotation, Customer, or other ERPNext commercial records.
