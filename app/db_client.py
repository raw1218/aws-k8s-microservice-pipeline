import os

import psycopg2
from psycopg2 import OperationalError, sql

CREATE_LOGS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS api_logs (
  id SERIAL PRIMARY KEY,
  client_ip TEXT NOT NULL,
  info TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);
"""


class DbClient:
    """
    Simple synchronous DB client for demos.

    Usage:
      client = DbClient.from_env()
      client.insert_request_log("1.2.3.4", "request info")

    Notes:
    - This implementation is intentionally synchronous and opens a new
      connection per call (simple and easy to reason about).
    - For production or higher throughput replace with a connection pool
      or an async driver. If you call these methods from async FastAPI
      handlers they will block the event loop.
    """

    def __init__(self):
        self._dsn = self.from_env()
        self._initialized = False

    @classmethod
    def from_env() -> "DbClient":
        host = os.getenv("DATABASE_HOST", "postgres")
        port = os.getenv("DATABASE_PORT", "5432")
        user = os.getenv("POSTGRES_USER", "metrics_user")
        password = os.getenv("POSTGRES_PASSWORD", "password")
        db = os.getenv("POSTGRES_DB", "metrics_db")
        dsn = f"dbname={db} user={user} password={password} host={host} port={port}"
        return dsn

    def _connect(self):
        """Open and return a new psycopg2 connection."""
        return psycopg2.connect(self._dsn)

    def ensure_table(self) -> None:
        """
        Create the table if it does not exist.
        Idempotent per-instance using self._initialized to avoid repeated DDL.
        """
        if self._initialized:
            return
        try:
            conn = self._connect()
            conn.autocommit = True
            with conn.cursor() as cur:
                cur.execute(CREATE_LOGS_TABLE_SQL)
            conn.close()
            self._initialized = True
        except Exception:
            # best-effort for demo: swallow errors so the app keeps running
            return

    def insert_request_log(self, client_ip: str, info: str) -> None:
        """
        Insert a log row synchronously.
        Opens a connection, performs the insert, and closes the connection.
        """
        try:
            # ensure table exists once per instance
            self.ensure_table()
            conn = self._connect()
            conn.autocommit = True
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO api_logs (client_ip, info) VALUES (%s, %s)",
                    (client_ip, info),
                )
            conn.close()
        except Exception:
            # best-effort logging; ignore failures for now
            return

    def close(self) -> None:
        """Placeholder if you add pooled resources later."""
        return