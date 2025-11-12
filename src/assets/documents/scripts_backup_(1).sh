#!/bin/bash

# SPLANTS Marketing Engine - Database Backup Script

set -e

# Configuration
BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="splants_backup_${TIMESTAMP}.sql"

# Create backup directory if it doesn't exist
mkdir -p ${BACKUP_DIR}

echo "================================================"
echo "SPLANTS Database Backup"
echo "================================================"
echo ""

# Perform backup
echo "Creating backup..."
docker-compose exec -T db pg_dump -U splants splants > ${BACKUP_DIR}/${BACKUP_FILE}

# Compress backup
echo "Compressing backup..."
gzip ${BACKUP_DIR}/${BACKUP_FILE}

# Get file size
SIZE=$(ls -lh ${BACKUP_DIR}/${BACKUP_FILE}.gz | awk '{print $5}')

echo ""
echo "✅ Backup complete!"
echo "   File: ${BACKUP_DIR}/${BACKUP_FILE}.gz"
echo "   Size: ${SIZE}"
echo ""

# Keep only last 7 backups
echo "Cleaning old backups (keeping last 7)..."
ls -t ${BACKUP_DIR}/splants_backup_*.sql.gz | tail -n +8 | xargs -r rm

echo "Done!"