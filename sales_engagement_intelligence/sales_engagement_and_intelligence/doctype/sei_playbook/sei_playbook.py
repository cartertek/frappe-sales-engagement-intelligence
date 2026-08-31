from __future__ import annotations

import frappe
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

@frappe.whitelist()
def assign_signal_type(playbook: str, signal_type: str) -> None:
    """Assign an existing Signal Type to this Playbook using the canonical Link field."""
    playbook_doc = frappe.get_doc("SEI Playbook", playbook)
    playbook_doc.check_permission("write")
    signal_type_doc = frappe.get_doc("SEI Signal Type", signal_type)
    signal_type_doc.check_permission("write")
    signal_type_doc.playbook = playbook_doc.name
    signal_type_doc.save()


@frappe.whitelist()
def update_signal_type_from_playbook(
    playbook: str,
    signal_type: str,
    category: str,
    research_arena: str,
    active: int | str | bool,
) -> None:
    """Edit canonical Signal Type fields from the Playbook management table."""
    playbook_doc = frappe.get_doc("SEI Playbook", playbook)
    playbook_doc.check_permission("write")
    signal_type_doc = frappe.get_doc("SEI Signal Type", signal_type)
    signal_type_doc.check_permission("write")
    if signal_type_doc.playbook != playbook_doc.name:
        frappe.throw(f"Signal Type {signal_type} is no longer assigned to Playbook {playbook}.")
    signal_type_doc.category = category
    signal_type_doc.research_arena = research_arena
    signal_type_doc.active = frappe.utils.cint(active)
    signal_type_doc.save()


@frappe.whitelist()
def move_signal_type(signal_type: str, from_playbook: str, to_playbook: str) -> None:
    """Move a Signal Type from one Playbook to another without creating duplicate relationship rows."""
    source = frappe.get_doc("SEI Playbook", from_playbook)
    source.check_permission("write")
    target = frappe.get_doc("SEI Playbook", to_playbook)
    target.check_permission("write")
    signal_type_doc = frappe.get_doc("SEI Signal Type", signal_type)
    signal_type_doc.check_permission("write")
    if signal_type_doc.playbook != source.name:
        frappe.throw(f"Signal Type {signal_type} is no longer assigned to Playbook {from_playbook}.")
    signal_type_doc.playbook = target.name
    signal_type_doc.save()
