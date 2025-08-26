"""
Database migration script (placeholder).  Creates core tables for the trading system.

This script uses SQL statements to set up the database schema defined in the design.
Run with the appropriate DATABASE_URL environment variable.
"""

import os
import psycopg2


def run_migrations() -> None:
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL not set")
    conn = psycopg2.connect(url)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS positions (
            id SERIAL PRIMARY KEY,
            symbol TEXT NOT NULL,
            qty NUMERIC NOT NULL,
            avg_entry NUMERIC NOT NULL,
            unrealised_pnl NUMERIC NOT NULL DEFAULT 0,
            realised_pnl NUMERIC NOT NULL DEFAULT 0,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        """
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Migrations completed")


if __name__ == "__main__":
    run_migrations()