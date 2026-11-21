#!/usr/bin/env bash
# Pulls a timestamped backup of server A's /var/www/html to server B.
# Run hourly by cron as root (see cron/www-backup).
set -uo pipefail

SOURCE="ubuntu@192.168.1.222:/var/www/html/"
BACKUP_ROOT="/var/backups/www-from-a"
SSH_KEY="/root/.ssh/sync_ed25519"
LOG_FILE="/var/log/www-backup.log"
KEEP=48   # keep the newest 48 hourly backups (2 days)

TIMESTAMP=$(date '+%Y-%m-%d_%H%M')
TARGET="$BACKUP_ROOT/$TIMESTAMP"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') $1" >> "$LOG_FILE"
}

mkdir -p "$BACKUP_ROOT"
chmod 700 "$BACKUP_ROOT"

if rsync -a -e "ssh -i $SSH_KEY -o BatchMode=yes" "$SOURCE" "$TARGET/"; then
    log "OK $TARGET"
else
    log "FAILED $TARGET (rsync exit code $?)"
    exit 1
fi

# Remove all but the newest $KEEP backups
ls -1d "$BACKUP_ROOT"/*/ | head -n -"$KEEP" | xargs -r rm -rf
