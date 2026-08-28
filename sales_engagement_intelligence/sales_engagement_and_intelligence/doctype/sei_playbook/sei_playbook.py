from __future__ import annotations

from frappe.model.document import Document


class SEIPlaybook(Document):
    def validate(self) -> None:
        from sales_engagement_intelligence.sales_engagement_and_intelligence.services import (
            playbook_arena_sync,
        )

        playbook_arena_sync.validate_playbook_relationships(self)

    def on_update(self) -> None:
        from sales_engagement_intelligence.sales_engagement_and_intelligence.services import (
            playbook_arena_sync,
        )

        playbook_arena_sync.sync_from_playbook(self)

        if self.has_value_changed("signal_qualification_script"):
            from sales_engagement_intelligence.sales_engagement_and_intelligence.services import qualification

            qualification.recalculate_prospects_for_playbook(self.name)
