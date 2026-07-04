import click
import frappe


def after_install() -> None:
    """Run lightweight post-install setup for SEI."""

    try:
        print("Setting up Sales Engagement and Intelligence...")
        frappe.clear_cache()
        click.secho("Thank you for installing Sales Engagement and Intelligence!", fg="green")
    except Exception as exc:
        click.secho("Sales Engagement and Intelligence installation failed.", fg="bright_red")
        raise exc
