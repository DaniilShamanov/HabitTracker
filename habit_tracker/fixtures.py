"""Predefined habits and 4-week check-off fixture data."""

from __future__ import annotations

from datetime import datetime, timedelta

from .models import Periodicity

PREDEFINED_HABITS = [
    ("Drink Water", "Drink at least 2 liters of water", Periodicity.DAILY, 1, 1),
    ("Read", "Read at least 20 minutes", Periodicity.DAILY, 1, 1),
    ("Meditate", "10-minute mindfulness session", Periodicity.DAILY, 1, 1),
    ("Workout", "Complete a workout session", Periodicity.WEEKLY, 7, 1),
    ("Plan Week", "Review and plan weekly goals", Periodicity.WEEKLY, 7, 1),
    ("Budget Review", "Check monthly spending and savings", Periodicity.MONTHLY, 30, 1),
    ("Tax Prep", "Prepare annual tax documents", Periodicity.YEARLY, 365, 1),
    ("Deep Clean", "Clean one room thoroughly", Periodicity.CUSTOM, 10, 1),
]


def four_week_fixture(start: datetime | None = None) -> dict[str, list[datetime]]:
    """Return four weeks of sample completion data for predefined habits."""
    start_date = (start or datetime(2026, 2, 1, 8, 0, 0)).replace(hour=8, minute=0, second=0, microsecond=0)

    def daily(days: list[int]) -> list[datetime]:
        return [start_date + timedelta(days=offset) for offset in days]

    def weekly(weeks: list[int]) -> list[datetime]:
        return [start_date + timedelta(weeks=offset, days=1) for offset in weeks]

    return {
        "Drink Water": daily(list(range(0, 28))),
        "Read": daily([d for d in range(0, 28) if d not in {6, 13, 20}]),
        "Meditate": daily([0, 1, 3, 4, 7, 8, 9, 14, 15, 16, 22, 23, 24]),
        "Workout": weekly([0, 1, 2, 3]),
        "Plan Week": weekly([0, 2, 3]),
        "Budget Review": [start_date - timedelta(days=15), start_date + timedelta(days=20)],
        "Tax Prep": [start_date - timedelta(days=365), start_date],
        "Deep Clean": [start_date + timedelta(days=d) for d in [0, 10, 20]],
    }
