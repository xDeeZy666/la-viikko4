# Linux administration Week 4

Server B is a clone of server A (cPouta snapshot). B pulls hourly backups of A's
website files and keeps a read-only replica of A's MariaDB database.

- Server A: http://195.148.23.171/viikko2/
- Server B: http://195.148.20.47/viikko4/

## Files
- `backup-www-from-a.sh` + `cron/www-backup` – hourly backup from A to B
- `replication/` – MariaDB settings for A and B
- `app.py`, `templates/`, `systemd/`, `nginx/` – read-only viikko4 app on B
