"""SQLite persistence layer for habits and check-offs."""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable

from .models import Habit, Periodicity


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
                    periodicity TEXT NOT NULL CHECK (periodicity IN ('daily', 'weekly')),
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

    def create_habit(self, name: str, description: str, periodicity: Periodicity) -> Habit:
        """Create and return a new habit."""
        created_at = datetime.now(UTC).isoformat(timespec="seconds")
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO habits (name, description, periodicity, created_at) VALUES (?, ?, ?, ?)",
                (name, description, periodicity.value, created_at),
            )
            habit_id = cur.lastrowid
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
                "SELECT id, name, description, periodicity, created_at FROM habits ORDER BY id"
            ).fetchall()
        return [self._row_to_habit(row) for row in rows]

    def list_habits_by_periodicity(self, periodicity: Periodicity) -> list[Habit]:
        """Return habits filtered by periodicity."""
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, name, description, periodicity, created_at
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
                "SELECT id, name, description, periodicity, created_at FROM habits WHERE id = ?",
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

    def load_fixture_data(self, habits: Iterable[tuple[str, str, Periodicity]], fixture: dict[str, list[datetime]]) -> None:
        """Insert predefined habits and completion history for testing/demo purposes."""
        created: dict[str, int] = {}
        for name, description, periodicity in habits:
            habit = self.create_habit(name, description, periodicity)
            created[name] = habit.id

        for habit_name, timestamps in fixture.items():
            habit_id = created[habit_name]
            for timestamp in timestamps:
                self.complete_habit(habit_id, timestamp)

    @staticmethod
    def _row_to_habit(row: sqlite3.Row) -> Habit:
        return Habit(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            periodicity=Periodicity(row["periodicity"]),
            created_at=datetime.fromisoformat(row["created_at"]),
        )
