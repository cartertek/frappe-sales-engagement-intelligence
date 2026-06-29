# Site and Environment Baseline

Complete this checklist against the target Frappe/ERPNext/Frappe CRM site before beginning Milestone 2 data model work.

## Target Site

```text
Target site: TBD
Bench path: TBD
ERPNext version: TBD
Frappe CRM version: TBD
Frappe version: TBD
Python version: TBD
Node version: TBD
MariaDB version: TBD
Redis status: TBD
```

## Discovery Commands

```bash
bench --site all list-apps
ls sites
bench version
python --version
node --version
mysql --version
bench --site <site-name> doctor
```

## Migration Check

```bash
bench --site <site-name> migrate
bench build
```

If the deployment runs in production mode, restart through the environment's normal process:

```bash
bench restart
```

For Dockerized deployments, use the relevant compose/container restart workflow instead of assuming direct supervisor control.

## Backup Baseline

```bash
bench --site <site-name> backup --with-files
ls -lh sites/<site-name>/private/backups/
```

Minimum confirmation before Milestone 2:

- Database backup works
- Private files backup works
- Public files backup works
- Backup location is known
- Restore procedure is understood
