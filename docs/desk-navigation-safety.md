# Frappe v17 Desk Navigation Safety

This app must not maintain Frappe v17 global Desk navigation state directly.

The restore incident showed that these records are shared site-wide and can affect every installed app:

- `Workspace`
- `Workspace Sidebar`
- `Desktop Icon`
- `Desktop Layout`
- `User Workspaces`

## Rules

1. Keep SEI pages as source-controlled `Workspace` records only.
2. Do not ship `Desktop Icon` fixtures.
3. Do not ship `Workspace Sidebar` fixtures.
4. Do not mutate `Desktop Layout` or `User Workspaces` from this app.
5. Do not patch the global Desk sidebar/frontend renderer by matching labels.
6. Do not create app records with generic global document names such as `Assets`, `Reports`, `Settings`, or `CRM`.
7. Do not mechanically prefix every file or record. Use a namespace only where the Frappe document name is global or where the field is installed into another app's DocType.

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

If Desk navigation is broken, restore a known-good site backup before deploying app changes. Do not attempt to repair the global menu by synthesizing `Desktop Icon`, `Workspace Sidebar`, `Desktop Layout`, or `User Workspaces` rows from this app.

After deploy, verify:

- ERPNext loads.
- Frappe CRM loads.
- The global Desk menu is unchanged outside the Sales Engagement and Intelligence app.
- The Sales Engagement and Intelligence workspace loads and shows only SEI-owned shortcuts.
