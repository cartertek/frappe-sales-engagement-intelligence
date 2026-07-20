from __future__ import annotations

import frappe

SYNC_FLAG = "sei_syncing_playbook_arenas"


def validate_playbook_relationships(playbook) -> None:
    if getattr(frappe.flags, SYNC_FLAG, False) or playbook.is_new():
        return
    selected = {row.research_arena for row in playbook.get("research_arenas") or [] if row.research_arena}
    rows = frappe.get_all(
        "SEI Signal Type", filters={"playbook": playbook.name}, fields=["name", "research_arena"]
    )
    for row in rows:
        if row.research_arena and row.research_arena not in selected:
            frappe.throw(
                f"Playbook {playbook.name} cannot be unassigned from Research Arena "
                f"{row.research_arena} because Signal Type {row.name} uses this pairing."
            )


def validate_arena_relationships(arena) -> None:
    if getattr(frappe.flags, SYNC_FLAG, False) or arena.is_new():
        return
    selected = {row.playbook for row in arena.get("assigned_playbooks") or [] if row.playbook}
    rows = frappe.get_all(
        "SEI Signal Type", filters={"research_arena": arena.name}, fields=["name", "playbook"]
    )
    for row in rows:
        if row.playbook and row.playbook not in selected:
            frappe.throw(
                f"Playbook {row.playbook} cannot be unassigned from Research Arena {arena.name} "
                f"because Signal Type {row.name} uses this pairing."
            )


def sync_from_playbook(playbook) -> None:
    if getattr(frappe.flags, SYNC_FLAG, False):
        return
    selected = {row.research_arena for row in playbook.get("research_arenas") or [] if row.research_arena}
    _sync_counterpart_rows(
        counterpart_doctype="SEI Research Arena",
        counterpart_field="assigned_playbooks",
        link_field="playbook",
        source_name=playbook.name,
        selected_names=selected,
    )


def sync_from_arena(arena) -> None:
    if getattr(frappe.flags, SYNC_FLAG, False):
        return
    selected = {row.playbook for row in arena.get("assigned_playbooks") or [] if row.playbook}
    _sync_counterpart_rows(
        counterpart_doctype="SEI Playbook",
        counterpart_field="research_arenas",
        link_field="research_arena",
        source_name=arena.name,
        selected_names=selected,
    )


def _sync_counterpart_rows(
    *, counterpart_doctype, counterpart_field, link_field, source_name, selected_names
):
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
