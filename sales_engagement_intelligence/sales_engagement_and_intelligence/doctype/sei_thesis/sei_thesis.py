from frappe.model.document import Document


class SEIThesis(Document):
    def validate(self):
        from sales_engagement_intelligence.sales_engagement_and_intelligence.services import (
            thesis_arena_sync,
        )

        thesis_arena_sync.validate_thesis_relationships(self)

    def on_update(self):
        from sales_engagement_intelligence.sales_engagement_and_intelligence.services import (
            thesis_arena_sync,
        )

        thesis_arena_sync.sync_from_thesis(self)
