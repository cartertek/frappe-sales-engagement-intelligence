from __future__ import annotations

import frappe
from frappe.model.document import Document


class SEISignalType(Document):
    def validate(self):
        self.validate_thesis_arena_pair()

    def validate_thesis_arena_pair(self) -> None:
        if not self.thesis or not self.research_arena:
            return
        allowed = frappe.db.exists(
            "SEI Thesis Research Arena",
            {
                "parent": self.thesis,
                "parenttype": "SEI Thesis",
                "parentfield": "research_arenas",
                "research_arena": self.research_arena,
            },
        )
        if not allowed:
            frappe.throw(
                f"Research Arena {self.research_arena} is not assigned to Thesis {self.thesis}."
            )
