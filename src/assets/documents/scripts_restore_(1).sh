#!/bin/bash

# SPLANTS Marketing Engine - Database Restore Script

set -e

echo "================================================"
echo "SPLANTS Database Restore"
echo "================================================"
echo ""

# Check for backup file argument
if [ $# -eq 0 ]; then
    echo "Usage: ./scripts/restore.sh <backup-file>"
    echo ""
    echo "Available backups:"
    ls -la ./backups/*.sql.gz 2>/dev/null || echo "No backups found"
    exit 1
fi

BACKUP_FILE=$1

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "⚠️  WARNING: This will replace all current data!"
read -p "Are you sure you want to restore from $BACKUP_FILE? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Restore cancelled"
    exit 0
fi

echo "Restoring database..."

# Decompress if needed
if [[ $BACKUP_FILE == *.gz ]]; then
    echo "Decompressing backup..."
    gunzip -c $BACKUP_FILE | docker-compose exec -T db psql -U splants splants
else
    docker-compose exec -T db psql -U splants splants < $BACKUP_FILE
fi

echo ""
echo "✅ Database restored successfully!"
echo ""
echo "You may need to restart the application:"
echo "  docker-compose restart app"