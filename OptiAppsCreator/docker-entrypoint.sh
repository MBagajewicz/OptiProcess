#!/bin/sh
set -eu

export AUTH_DB_PATH="${AUTH_DB_PATH:-/data/users.db}"
users_file="${USERS_IMPORT_FILE:-/deployment/users_import.xlsx}"

if [ -f "$users_file" ]; then
    echo "Importing new users from $users_file"
    python /app/init_users_from_excel.py --file "$users_file" --skip-existing
fi

exec "$@"
