# Prospect Review

Prospect review confirms that research records, evidence, and resulting Frappe workflow state are correct.

Review the SEI Prospect form for identity, Research Arena, source URL, offer, signal summary, notes, contact path, qualification status, lifecycle status, and CRM links. Review related SEI Signal records and their managed Signal Types to confirm the derived thesis list, evidence, and timing are current and specific.

Use the queue shortcuts in the Prospecting workspace:

- Needs Research: insufficient evidence or context; continue research before dispositioning.
- Research Complete: research is complete and the prospect is awaiting the next appropriate workflow action.
- Rejected: Frappe rejected the prospect based on the evaluated signal strengths; the prospect should not continue unless intentionally reopened.
- Find Contact: prospect looks relevant but no usable contact path exists. Use [Prospect identity and contact research](identity-contact-research.md) to complete identity context, select primary contact roles, and research validated contacts.
- Qualified: Frappe qualified the prospect based on the evaluated signal strengths, but CRM conversion has not been prepared.
- Ready for CRM Conversion: explicit operator action marked the prospect ready.
- Do Not Contact: protected suppression state.

Do Not Contact and Rejected states are protected. Do not bypass them through API updates, import fixes, or CRM conversion actions.
