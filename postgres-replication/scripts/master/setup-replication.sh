#!/bin/bash
set -e

# Create replication role
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'replicapassword';
    ALTER SYSTEM SET wal_level = replica;
    ALTER SYSTEM SET max_wal_senders = 10;
    ALTER SYSTEM SET wal_keep_size = 64;
    ALTER SYSTEM SET archive_mode = on;
    ALTER SYSTEM SET archive_command = 'cp %p /var/lib/postgresql/data/archive/%f';
    SELECT pg_reload_conf();
EOSQL

mkdir -p /var/lib/postgresql/data/archive
