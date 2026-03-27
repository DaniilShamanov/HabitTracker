"""SQLite persistence layer for habits and check-offs."""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable

from .models import Habit, Periodicity

DEFAULT_INTERVAL_DAYS = {
        Periodicity.DAILY: 1,
        Periodicity.WEEKLY: 7,
        Periodicity.MONTHLY: 30,      # approximate
        Periodicity.YEARLY: 365,      # approximate
        Periodicity.CUSTOM: 1,        # fallback, but should be set explicitly
    }


class HabitAlreadyExistsError(ValueError):
    """Raised when trying to create a habit with a duplicate name."""


class HabitRepository:
    """Repository object that stores and retrieves habits in SQLite."""

    def __init__(self, db_path: str = "habits.db") -> None:
        self.db_path = Path(db_path)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def initialize(self) -> None:
        """Create tables when they do not exist."""
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT NOT NULL,
                    periodicity TEXT NOT NULL CHECK (periodicity IN ('daily', 'weekly', 'monthly', 'yearly', 'custom')),
                    interval_days INTEGER NOT NULL DEFAULT 1 CHECK (interval_days > 0),
                    target_per_period INTEGER NOT NULL DEFAULT 1 CHECK (target_per_period > 0),
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS completions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER NOT NULL,
                    completed_at TEXT NOT NULL,
                    FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE
                );
                """
            )
            self._ensure_column(conn, "habits", "interval_days", "INTEGER NOT NULL DEFAULT 1")
            self._ensure_column(conn, "habits", "target_per_period", "INTEGER NOT NULL DEFAULT 1")

    @staticmethod
    def _ensure_column(conn: sqlite3.Connection, table: str, column: str, definition: str) -> None:
        existing = {row["name"] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}
        if column not in existing:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")

    def create_habit(
    self,
    name: str,
    description: str,
    periodicity: Periodicity,
    interval_days: int | None = None,
    target_per_period: int = 1,
) -> Habit:
        """Create and return a new habit."""
        resolved_interval = interval_days or DEFAULT_INTERVAL_DAYS[periodicity]
        created_at = datetime.now(UTC).isoformat(timespec="seconds")
        try:
            with self._connect() as conn:
                cur = conn.execute(
                    "INSERT INTO habits (name, description, periodicity, interval_days, target_per_period, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (name, description, periodicity.value, resolved_interval, target_per_period, created_at),
                )
                habit_id = cur.lastrowid
        except sqlite3.IntegrityError as exc:
            raise HabitAlreadyExistsError(f"Habit named '{name}' already exists") from exc
        return self.get_habit_by_id(int(habit_id))

    def delete_habit(self, habit_id: int) -> None:
        """Delete a habit and all its completion records."""
        with self._connect() as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("DELETE FROM habits WHERE id = ?", (habit_id,))

    def list_habits(self) -> list[Habit]:
        """Return all currently tracked habits."""
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, name, description, periodicity, interval_days, target_per_period, created_at
                FROM habits ORDER BY id
                """
            ).fetchall()
        return [self._row_to_habit(row) for row in rows]

    def list_habits_by_periodicity(self, periodicity: Periodicity) -> list[Habit]:
        """Return habits filtered by periodicity."""
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, name, description, periodicity, interval_days, target_per_period, created_at
                FROM habits
                WHERE periodicity = ?
                ORDER BY id
                """,
                (periodicity.value,),
            ).fetchall()
        return [self._row_to_habit(row) for row in rows]

    def get_habit_by_id(self, habit_id: int) -> Habit:
        """Return one habit by id."""
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT id, name, description, periodicity, interval_days, target_per_period, created_at
                FROM habits WHERE id = ?
                """,
                (habit_id,),
            ).fetchone()
        if row is None:
            raise ValueError(f"Habit with id={habit_id} not found")
        return self._row_to_habit(row)

    def complete_habit(self, habit_id: int, completed_at: datetime | None = None) -> None:
        """Insert a check-off timestamp for a habit."""
        timestamp = (completed_at or datetime.now(UTC)).isoformat(timespec="seconds")
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO completions (habit_id, completed_at) VALUES (?, ?)",
                (habit_id, timestamp),
            )

    def list_completions(self, habit_id: int) -> list[datetime]:
        """List completion datetimes for a habit."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT completed_at FROM completions WHERE habit_id = ? ORDER BY completed_at",
                (habit_id,),
            ).fetchall()
        return [datetime.fromisoformat(row["completed_at"]) for row in rows]

    def load_fixture_data(self, habits: Iterable[tuple], fixture: dict[str, list[datetime]]) -> None:
        """Insert predefined habits and completion history for testing/demo purposes."""
        created: dict[str, int] = {}
        for raw in habits:
            if len(raw) == 3:
                name, description, periodicity = raw
                habit = self.create_habit(name, description, periodicity)
            else:
                name, description, periodicity, interval_days, target_per_period = raw
                habit = self.create_habit(
                    name,
                    description,
                    periodicity,
                    interval_days=interval_days,
                    target_per_period=target_per_period,
                )
            created[name] = habit.id

        for habit_name, timestamps in fixture.items():
            habit_id = created[habit_name]
            for timestamp in timestamps:
                self.complete_habit(habit_id, timestamp)

    @staticmethod
    def _row_to_habit(row: sqlite3.Row) -> Habit:
        periodicity = Periodicity(row["periodicity"])
        interval_days = row["interval_days"] if row["interval_days"] else DEFAULT_INTERVAL_DAYS[periodicity]
        return Habit(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            periodicity=periodicity,
            interval_days=interval_days,
            target_per_period=row["target_per_period"] or 1,
            created_at=datetime.fromisoformat(row["created_at"]),
        )
