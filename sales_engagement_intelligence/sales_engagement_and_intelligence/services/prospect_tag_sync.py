from __future__ import annotations

import frappe

TRIGGER_NAME = "sei_sync_signal_prospect_tags_au"


def sync_signal_prospect_tags(prospect: str | None) -> None:
    """Copy a prospect's current Frappe tags onto all linked SEI Signals."""

    if not prospect:
        return

    ensure_prospect_user_tags_column()
    if not _can_sync():
        return

    tags = frappe.db.get_value("SEI Prospect", prospect, "_user_tags", ignore=True) or ""
    frappe.db.sql(
        """
        UPDATE `tabSEI Signal`
        SET prospect_tags = %(tags)s
        WHERE prospect = %(prospect)s
        """,
        {"tags": tags, "prospect": prospect},
    )


def sync_all_signal_prospect_tags() -> None:
    """Backfill all SEI Signal prospect tag snapshots from linked prospects."""

    ensure_prospect_user_tags_column()
    if not _can_sync():
        return

    frappe.db.sql(
        """
        UPDATE `tabSEI Signal` AS sig
        LEFT JOIN `tabSEI Prospect` AS prospect ON prospect.name = sig.prospect
        SET sig.prospect_tags = COALESCE(prospect._user_tags, '')
        """
    )


def ensure_signal_prospect_tag_trigger() -> None:
    """Install the DB-level trigger that keeps signal prospect tags current.

    Frappe's tag UI updates `_user_tags` with `frappe.db.set_value(..., update_modified=False)`
    and does not save the target document. A DocType hook on SEI Prospect therefore does
    not reliably run when tags change. This trigger ties synchronization to the database
    update of `tabSEI Prospect._user_tags` itself, which covers normal tag add/remove,
    bulk tag operations, and direct `_user_tags` updates.
    """

    ensure_prospect_user_tags_column()
    if not _can_sync():
        return

    if not _is_mariadb():
        frappe.log_error(
            title="SEI prospect tag sync trigger skipped",
            message="Automatic signal prospect tag synchronization currently requires MariaDB.",
        )
        return

    frappe.db.sql(f"DROP TRIGGER IF EXISTS `{TRIGGER_NAME}`")
    frappe.db.sql(
        f"""
        CREATE TRIGGER `{TRIGGER_NAME}`
        AFTER UPDATE ON `tabSEI Prospect`
        FOR EACH ROW
        BEGIN
            IF NOT (OLD._user_tags <=> NEW._user_tags) THEN
                UPDATE `tabSEI Signal`
                SET prospect_tags = COALESCE(NEW._user_tags, '')
                WHERE prospect = NEW.name;
            END IF;
        END
        """
    )


def drop_signal_prospect_tag_trigger() -> None:
    if _is_mariadb():
        frappe.db.sql(f"DROP TRIGGER IF EXISTS `{TRIGGER_NAME}`")


def ensure_prospect_user_tags_column() -> None:
    """Create SEI Prospect's optional Frappe `_user_tags` column before installing sync."""

    if not frappe.db.table_exists("SEI Prospect"):
        return
    if frappe.db.has_column("SEI Prospect", "_user_tags"):
        return

    from frappe.desk.doctype.tag.tag import DocTags

    DocTags("SEI Prospect").setup()
    frappe.client_cache.delete_value("table_columns::tabSEI Prospect")


def _can_sync() -> bool:
    return (
        frappe.db.table_exists("SEI Prospect")
        and frappe.db.table_exists("SEI Signal")
        and frappe.db.has_column("SEI Prospect", "_user_tags")
        and frappe.db.has_column("SEI Signal", "prospect_tags")
    )


def _is_mariadb() -> bool:
    return (getattr(frappe.db, "db_type", None) or "mariadb") == "mariadb"
