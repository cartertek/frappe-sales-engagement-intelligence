# Queue API

Methods:

- `get_needs_research_queue(filters=None, limit=50)`
- `get_ready_for_crm_conversion_queue(filters=None, limit=50)`
- `get_find_contact_queue(filters=None, limit=50)`
- `get_protected_status_queue(filters=None, limit=50)` manager-only
- `get_recent_import_batches(filters=None, limit=50)`

Queue endpoints are direct DocType queries over SEI data and workflow fields. They do not call Milestone 6 reports or require report objects to exist.
