from __future__ import annotations

import frappe
from frappe.model.document import Document


class SEIPlaybook(Document):
    def validate(self) -> None:
        self.remove_blank_signal_rules()
        self.validate_signal_types()
        from sales_engagement_intelligence.sales_engagement_and_intelligence.services import (
            playbook_arena_sync,
        )

        playbook_arena_sync.validate_playbook_relationships(self)

    def on_update(self) -> None:
        self.sync_signal_type_links()
        from sales_engagement_intelligence.sales_engagement_and_intelligence.services import (
            playbook_arena_sync,
        )

        playbook_arena_sync.sync_from_playbook(self)


    def remove_blank_signal_rules(self) -> None:
        """Discard placeholder rows that contain no rule data."""
        rows = []
        for row in self.get("signal_rules") or []:
            values = (
                row.get("signal_type"),
                row.get("minimum_strength"),
                row.get("evidence_basis_required"),
                row.get("exclude_from_qualification"),
                row.get("notes"),
            )
            if any(value.strip() if isinstance(value, str) else value for value in values):
                rows.append(row)
        self.set("signal_rules", rows)

    def validate_signal_types(self) -> None:
        seen: set[str] = set()
        allowed_arenas = {
            row.research_arena for row in (self.get("research_arenas") or []) if row.research_arena
        }

        for row in self.get("signal_types") or []:
            if row.signal_type in seen:
                frappe.throw(f"Signal Type {row.signal_type} appears more than once.")
            seen.add(row.signal_type)

            arena = frappe.db.get_value("SEI Signal Type", row.signal_type, "research_arena")
            if arena and arena not in allowed_arenas:
                frappe.throw(
                    f"Signal Type {row.signal_type} uses Research Arena {arena}, which is not assigned "
                    f"to Playbook {self.name}."
                )

        if not self.is_new():
            assigned = frappe.get_all("SEI Signal Type", filters={"playbook": self.name}, pluck="name")
            removed = sorted(set(assigned) - seen)
            if removed:
                frappe.throw(
                    "Signal Types cannot be left without a Playbook. Move these Signal Types to another "
                    "Playbook before removing them: " + ", ".join(removed)
                )

    def sync_signal_type_links(self) -> None:
        if getattr(frappe.flags, "sei_syncing_playbook_signal_types", False):
            return

        try:
            frappe.flags.sei_syncing_playbook_signal_types = True
            for row in self.get("signal_types") or []:
                current = frappe.db.get_value("SEI Signal Type", row.signal_type, "playbook")
                if current != self.name:
                    frappe.db.set_value(
                        "SEI Signal Type",
                        row.signal_type,
                        "playbook",
                        self.name,
                        update_modified=True,
                    )
                frappe.db.delete(
                    "SEI Playbook Signal Type",
                    {
                        "signal_type": row.signal_type,
                        "parent": ["!=", self.name],
                    },
                )
        finally:
            frappe.flags.sei_syncing_playbook_signal_types = False
