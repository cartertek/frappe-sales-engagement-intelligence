# Signal API

Methods:

- `add_signal(prospect, payload)`
- `update_signal(signal, payload)`
- `get_signals(prospect)`
- `find_duplicate_signal(prospect, payload)`

Adding or updating a signal recalculates Prospect qualification and lifecycle. Qualification behavior stays delegated to M3 services: inferred or weak signals do not automatically qualify a prospect.
