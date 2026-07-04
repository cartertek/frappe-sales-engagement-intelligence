# Frappe v17 Desk Navigation Safety

This app must preserve Frappe v17 Desk navigation without taking ownership of unrelated global Desk state.

The restore incident showed that these records are shared site-wide and can affect every installed app:

- `Workspace`
- `Workspace Sidebar`
- `Desktop Icon`
- `Desktop Layout`
- `User Workspaces`

## Rules

1. Keep SEI pages as source-controlled `Workspace` records.
2. Use Frappe's generated Desk navigation pattern for installed apps: `add_to_apps_screen` plus public Workspaces.
3. Do not ship `Desktop Icon` fixtures.
4. Do not ship `Workspace Sidebar` fixtures.
5. Because normal `bench migrate` does not rerun app-install navigation generation, keep a narrow `after_migrate` bridge that recreates only SEI `Desktop Icon` and `Workspace Sidebar` rows after orphan cleanup.
6. Preserve production desktop icon display. Keep existing visible SEI desktop icon labels, order, color, wrapping, and SVG logo URLs stable; route renamed Workspaces behind those labels when needed.
7. Do not mutate `User Workspaces` from this app.
8. Do not patch the global Desk sidebar/frontend renderer by matching labels.
9. Do not create app records with generic global document names such as `Assets`, `Reports`, `Settings`, or `CRM`.
10. Do not mechanically prefix every file or record. Use a namespace only where the Frappe document name is global or where the field is installed into another app's DocType.

## Workspace naming

Frappe workspace document names are global enough to collide with ERPNext, Frappe CRM, HRMS, or Framework workspaces.

Child workspaces should use domain-owned document names, not blanket app prefixes. Clean labels are fine when the global document name is also domain-owned enough for the installed stack.

| Workspace document name | Visible label |
| --- | --- |
| Prospecting | Prospecting |
| Signals | Signals |
| Touchpoints | Touchpoints |
| Theses and Assets | Theses and Assets |
| CRM Attribution | CRM Attribution |
| Engagement Reports | Reports |
| Engagement Settings | Settings |

The parent workspace remains:

| Workspace document name | Visible label |
| --- | --- |
| Sales Engagement and Intelligence | Sales Engagement and Intelligence |

## Deployment guidance

If Desk navigation is broken, restore a known-good site backup before deploying app changes. Do not attempt broad global menu repair from this app. Migration repairs must be narrow, deterministic, and limited to SEI-owned/generated navigation rows needed to preserve the existing desktop display.

After deploy, verify:

- ERPNext loads.
- Frappe CRM loads.
- The global Desk menu is unchanged outside the Sales Engagement and Intelligence app.
- Existing saved desktop layouts still show the same SEI icon labels, order, color, wrapping, and SVG graphics after the Workspace document renames.
- The Sales Engagement and Intelligence workspace loads and shows only SEI-owned shortcuts.
