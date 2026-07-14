# Prospect Review

Prospect review turns raw research into a decision about whether the prospect belongs in an outreach queue.

Review the SEI Prospect form for identity, source arena, source URL, thesis, offer, signal summary, notes, contact path, qualification status, lifecycle status, and CRM links. Review related SEI Signal records to confirm that the evidence is current and specific.

Use the queue shortcuts in the Prospecting workspace:

- Needs Research: insufficient evidence or context; continue research before dispositioning.
- Research Complete: evidence is complete enough for human review, normally because qualification is Needs Review.
- Rejected: research is complete and the prospect should not continue because no qualifying outreach evidence exists.
- Find Contact: prospect looks relevant but no usable contact path exists.
- Qualified: enough evidence exists, but CRM conversion has not been prepared.
- Ready for CRM Conversion: explicit operator action marked the prospect ready.
- Do Not Contact: protected suppression state.

Do Not Contact and Rejected states are protected. Do not bypass them through API updates, import fixes, or CRM conversion actions.
