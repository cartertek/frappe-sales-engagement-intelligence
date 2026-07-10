# Prepare CRM Conversion

Use queue and preview endpoints first: `get_ready_for_crm_conversion_queue`, `preview_crm_conversion`, and `find_crm_duplicates`.

Manager-only create/link endpoints may be used only after explicit user instruction. Scripts must respect protected status failures and structured error envelopes.

Do not create ERPNext Lead, Opportunity, Quotation, Customer, or other ERPNext commercial records.
