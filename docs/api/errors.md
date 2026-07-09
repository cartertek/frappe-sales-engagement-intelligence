# Error Format

Successful calls return `ok: true`. Expected failures return `ok: false` with an error code and message. Stack traces are logged server-side and are not returned to scripts.

Common error codes:

- `VALIDATION_ERROR`
- `PERMISSION_DENIED`
- `NOT_FOUND`
- `DUPLICATE_FOUND`
- `PROTECTED_STATE`
- `INVALID_PAYLOAD`
- `UNSUPPORTED_OPERATION`
- `SCHEMA_ERROR`
- `IMPORT_ERROR`
- `CRM_CONVERSION_BLOCKED`
