#!/bin/bash
# PostgreSQL 数据库备份脚本
# 每天自动备份 flask_app 数据库

BACKUP_DIR="$HOME/projects/flask-web/backups"
DB_NAME="flask_app"
DB_USER="postgres"
DB_HOST="localhost"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/flask_app_$TIMESTAMP.sql"

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 执行备份
/Applications/Postgres.app/Contents/Versions/18/bin/pg_dump \
    -U "$DB_USER" \
    -h "$DB_HOST" \
    -d "$DB_NAME" \
    -F p \
    > "$BACKUP_FILE"

# 压缩备份
gzip "$BACKUP_FILE"

# 删除 7 天前的备份
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +7 -delete

echo "✅ 备份完成: $BACKUP_FILE.gz"
