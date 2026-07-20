from frappe.model.document import Document


class SEIResearchArena(Document):
    def validate(self):
        from sales_engagement_intelligence.sales_engagement_and_intelligence.services import (
            playbook_arena_sync,
        )

        playbook_arena_sync.validate_arena_relationships(self)

    def on_update(self):
        from sales_engagement_intelligence.sales_engagement_and_intelligence.services import (
            playbook_arena_sync,
        )

        playbook_arena_sync.sync_from_arena(self)
