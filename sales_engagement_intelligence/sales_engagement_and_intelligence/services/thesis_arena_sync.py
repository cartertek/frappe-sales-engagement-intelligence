from __future__ import annotations

import frappe

SYNC_FLAG = "sei_syncing_thesis_arenas"


def validate_thesis_relationships(thesis) -> None:
    if getattr(frappe.flags, SYNC_FLAG, False) or thesis.is_new():
        return
    selected = {row.research_arena for row in thesis.get("research_arenas") or [] if row.research_arena}
    rows = frappe.get_all(
        "SEI Signal Type",
        filters={"thesis": thesis.name},
        fields=["name", "research_arena"],
    )
    for row in rows:
        if row.research_arena and row.research_arena not in selected:
            frappe.throw(
                f"Thesis {thesis.name} cannot be unassigned from Research Arena "
                f"{row.research_arena} because Signal Type {row.name} uses this pairing."
            )


def validate_arena_relationships(arena) -> None:
    if getattr(frappe.flags, SYNC_FLAG, False) or arena.is_new():
        return
    selected = {row.thesis for row in arena.get("assigned_theses") or [] if row.thesis}
    rows = frappe.get_all(
        "SEI Signal Type",
        filters={"research_arena": arena.name},
        fields=["name", "thesis"],
    )
    for row in rows:
        if row.thesis and row.thesis not in selected:
            frappe.throw(
                f"Thesis {row.thesis} cannot be unassigned from Research Arena {arena.name} "
                f"because Signal Type {row.name} uses this pairing."
            )


def sync_from_thesis(thesis) -> None:
    if getattr(frappe.flags, SYNC_FLAG, False):
        return
    selected = {row.research_arena for row in thesis.get("research_arenas") or [] if row.research_arena}
    _sync_counterpart_rows(
        counterpart_doctype="SEI Research Arena",
        counterpart_field="assigned_theses",
        link_field="thesis",
        source_name=thesis.name,
        selected_names=selected,
    )


def sync_from_arena(arena) -> None:
    if getattr(frappe.flags, SYNC_FLAG, False):
        return
    selected = {row.thesis for row in arena.get("assigned_theses") or [] if row.thesis}
    _sync_counterpart_rows(
        counterpart_doctype="SEI Thesis",
        counterpart_field="research_arenas",
        link_field="research_arena",
        source_name=arena.name,
        selected_names=selected,
    )


def _sync_counterpart_rows(
    *,
    counterpart_doctype: str,
    counterpart_field: str,
    link_field: str,
    source_name: str,
    selected_names: set[str],
) -> None:
    setattr(frappe.flags, SYNC_FLAG, True)
    try:
        for name in frappe.get_all(counterpart_doctype, pluck="name"):
            doc = frappe.get_doc(counterpart_doctype, name)
            current = [row.get(link_field) for row in doc.get(counterpart_field) or []]
            should_include = name in selected_names
            has_source = source_name in current
            if should_include == has_source:
                continue
            if should_include:
                doc.append(counterpart_field, {link_field: source_name})
            else:
                doc.set(
                    counterpart_field,
                    [row for row in doc.get(counterpart_field) or [] if row.get(link_field) != source_name],
                )
            doc.save(ignore_permissions=True)
    finally:
        setattr(frappe.flags, SYNC_FLAG, False)
