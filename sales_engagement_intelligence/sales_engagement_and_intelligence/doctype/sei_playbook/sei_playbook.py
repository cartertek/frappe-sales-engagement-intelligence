from __future__ import annotations

import frappe
from frappe.model.document import Document


class SEIPlaybook(Document):
    def validate(self) -> None:
        self.validate_signal_types()

    def on_update(self) -> None:
        self.sync_signal_type_links()

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
