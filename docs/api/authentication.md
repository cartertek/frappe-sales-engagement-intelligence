# Authentication and Roles

Use Frappe session auth or API key/secret authentication for a controlled integration user. Do not hard-code credentials in scripts.

Example header format:

```text
Authorization: token <api_key>:<api_secret>
```

Recommended roles:

- `Sales Engagement User`: create/update regular SEI records, add signals, fetch queues, preview CRM conversion, run dry-run imports.
- `Sales Engagement Manager`: all user capabilities plus protected workflow actions, real imports, CRM create/link/sync actions, and mutating hygiene utilities.

Every write endpoint checks server-side roles and DocType permissions. UI button visibility is not treated as authorization.
