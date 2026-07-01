# Site and Environment Baseline

Baseline captured from the target Dockerized Frappe/ERPNext/Frappe CRM site before beginning Milestone 2 data model work.

## Target Site

```text
Target site: frappe.localhost
Bench path: /home/frappe/frappe-bench
Frappe version: 17.0.0-dev UNVERSIONED
ERPNext version: 17.0.0-dev UNVERSIONED
HRMS version: 17.0.0-dev UNVERSIONED
Frappe CRM version: 2.0.0-dev UNVERSIONED
Sales Engagement and Intelligence version: 0.0.1 UNVERSIONED
Python version: 3.14.2
Node version: not present on backend/frontend runtime PATH in deployed containers
MariaDB version: 10.11.14-MariaDB
Redis cache URL: redis://redis-cache:6379
Redis queue/socketio URL: redis://redis-queue:6379
Database host: db:3306
Database name: _d784d59a1bea3422
Scheduler status: enabled for site frappe.localhost
```

## Installed Apps

```text
frappe                        17.0.0-dev UNVERSIONED
erpnext                       17.0.0-dev UNVERSIONED
hrms                          17.0.0-dev UNVERSIONED
sales_engagement_intelligence 0.0.1      UNVERSIONED
crm                           2.0.0-dev  UNVERSIONED
```

## Docker Notes

The stack is Dockerized. Do not assume direct supervisor or `bench restart` control. Deploy/restart should use the compose/container workflow from `frappe_docker`.

The backend container finalize step runs the deploy-time migration/cache clear sequence once per recreated backend container.

## Migration Check

`bench --site frappe.localhost migrate` has completed successfully during the latest deployment cycle.

## Backup Baseline

Known backup location:

```text
/home/frappe/frappe-bench/sites/frappe.localhost/private/backups/
```

Observed backup files:

```text
20260629_105405-frappe_localhost-database.sql.gz
20260629_105405-frappe_localhost-files.tar
20260629_105405-frappe_localhost-private-files.tar
20260629_105405-frappe_localhost-site_config_backup.json
```

Minimum confirmation before Milestone 2:

- Database backup exists.
- Private files backup exists.
- Public files backup exists.
- Backup location is known.
- Restore procedure still needs to be documented separately if/when needed.
