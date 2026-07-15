"""A tiny SQLite-backed key/value store for OAuth state.

Namespaced blobs (clients, transactions, auth codes, tokens) persist across
restarts so issued tokens keep working. Values are opaque JSON strings.
"""

from __future__ import annotations

import os
import sqlite3
import threading
import time


class KVStore:
    def __init__(self, db_path: str):
        directory = os.path.dirname(os.path.abspath(db_path))
        os.makedirs(directory, exist_ok=True)
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS kv (
                ns TEXT NOT NULL,
                k  TEXT NOT NULL,
                v  TEXT NOT NULL,
                expires_at REAL,
                PRIMARY KEY (ns, k)
            )
            """
        )
        self._conn.commit()

    def put(self, ns: str, key: str, value: str, expires_at: float | None = None) -> None:
        with self._lock:
            self._conn.execute(
                "INSERT OR REPLACE INTO kv (ns, k, v, expires_at) VALUES (?, ?, ?, ?)",
                (ns, key, value, expires_at),
            )
            self._conn.commit()

    def get(self, ns: str, key: str) -> str | None:
        with self._lock:
            row = self._conn.execute(
                "SELECT v, expires_at FROM kv WHERE ns = ? AND k = ?", (ns, key)
            ).fetchone()
        if row is None:
            return None
        value, expires_at = row
        if expires_at is not None and expires_at < time.time():
            self.delete(ns, key)
            return None
        return value

    def delete(self, ns: str, key: str) -> None:
        with self._lock:
            self._conn.execute("DELETE FROM kv WHERE ns = ? AND k = ?", (ns, key))
            self._conn.commit()

    def purge_expired(self) -> None:
        with self._lock:
            self._conn.execute(
                "DELETE FROM kv WHERE expires_at IS NOT NULL AND expires_at < ?",
                (time.time(),),
            )
            self._conn.commit()
