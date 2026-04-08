import os
import logging

import psycopg2
from psycopg2 import sql

logging.basicConfig(level=logging.INFO)

CREATE_LOGS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS api_logs (
  id SERIAL PRIMARY KEY,
  client_ip TEXT NOT NULL,
  info TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);
"""


class DbClient:
    def __init__(self):
        self._dsn = self.from_env()
        self._initialized = False
        logging.info(f"DBClient initialized with DSN: {self._dsn}")

    def from_env(self) -> str:
        host = os.getenv("DATABASE_HOST", "postgres")
        port = os.getenv("DATABASE_PORT", "5432")
        user = os.getenv("POSTGRES_USER", "metrics_user")
        password = os.getenv("POSTGRES_PASSWORD", "password")
        db = os.getenv("POSTGRES_DB", "postgres")

        dsn = f"dbname={db} user={user} password={password} host={host} port={port}"
        logging.info(f"Constructed DSN (host={host}, db={db}, user={user})")
        return dsn

    def _connect(self):
        logging.info("Attempting DB connection...")
        try:
            conn = psycopg2.connect(self._dsn)
            logging.info("DB connection successful")
            return conn
        except Exception:
            logging.exception("DB CONNECTION FAILED")
            raise

    def ensure_table(self) -> None:
        if self._initialized:
            return
        try:
            logging.info("Ensuring api_logs table exists...")
            conn = self._connect()
            conn.autocommit = True

            with conn.cursor() as cur:
                cur.execute(CREATE_LOGS_TABLE_SQL)

            conn.close()
            self._initialized = True
            logging.info("Table ensured successfully")

        except Exception:
            logging.exception("FAILED TO CREATE TABLE")
            return

    def insert_request_log(self, client_ip: str, info: str) -> None:
        try:
            logging.info(f"Inserting log: ip={client_ip}, info={info}")

            self.ensure_table()
            conn = self._connect()
            conn.autocommit = True

            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO api_logs (client_ip, info) VALUES (%s, %s)",
                    (client_ip, info),
                )

            conn.close()
            logging.info("Insert successful")

        except Exception:
            logging.exception("INSERT FAILED")
            return

    def read_request_logs(self, num_entries) -> list[dict]:
        try:
            logging.info(f"Reading last {num_entries} logs")

            conn = self._connect()

            with conn.cursor() as cur:
                logging.info("Executing SELECT query")

                cur.execute(
                    "SELECT client_ip, info, created_at FROM api_logs ORDER BY created_at DESC LIMIT %s",
                    (num_entries,)  # important: must be a tuple
                )

                rows = cur.fetchall()
                logging.info(f"Fetched {len(rows)} rows")

            conn.close()

            return [
                {"client_ip": row[0], "info": row[1], "created_at": row[2]}
                for row in rows
            ]

        except Exception:
            logging.exception("READ FAILED")
            return []

    def close(self) -> None:
        return