#!/usr/bin/env python3
"""Initialize/update OptiAppsCreator users from an Excel file.

Expected columns: username, email, password
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from auth_db import get_db_path, init_db, upsert_user


REQUIRED_COLUMNS = {"username", "email", "password"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Import users from Excel into the OptiHexx auth database")
    parser.add_argument("--file", required=True, help="Excel file path with username, email, password columns")
    parser.add_argument("--db", default=None, help="Optional SQLite DB path. Defaults to AUTH_DB_PATH/data/users.db")
    args = parser.parse_args()

    excel_path = Path(args.file)
    if not excel_path.exists():
        raise SystemExit(f"Excel file not found: {excel_path}")

    db_path = Path(args.db) if args.db else get_db_path()
    init_db(db_path)

    df = pd.read_excel(excel_path)
    normalized = {str(c).strip().lower(): c for c in df.columns}
    missing = REQUIRED_COLUMNS - set(normalized)
    if missing:
        raise SystemExit(f"Missing required columns: {', '.join(sorted(missing))}")

    count = 0
    for _, row in df.iterrows():
        username = str(row[normalized["username"]]).strip()
        email = str(row[normalized["email"]]).strip().lower()
        password = str(row[normalized["password"]])
        if not username or not email or not password:
            continue
        upsert_user(username, email, password, db_path=db_path)
        count += 1

    print(f"Imported {count} users into {db_path}")


if __name__ == "__main__":
    main()
