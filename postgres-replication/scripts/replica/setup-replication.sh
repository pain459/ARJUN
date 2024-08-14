#!/bin/bash
set -e

until pg_isready --host=$REPLICATE_FROM --username=postgres; do
  echo "Waiting for master to be ready..."
  sleep 2
done

PGPASSWORD=$POSTGRES_PASSWORD pg_basebackup -h $REPLICATE_FROM -D /var/lib/postgresql/data -U replicator -Fp -Xs -P -R

echo "standby_mode = 'on'" >> /var/lib/postgresql/data/postgresql.auto.conf
echo "primary_conninfo = 'host=$REPLICATE_FROM port=5432 user=replicator password=replicapassword'" >> /var/lib/postgresql/data/postgresql.auto.conf
echo "trigger_file = '/tmp/postgresql.trigger.5432'" >> /var/lib/postgresql/data/postgresql.auto.conf
