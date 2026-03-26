"""Functional analytics utilities for habit data."""

from __future__ import annotations

from datetime import datetime
from typing import Iterable

from .models import Habit, Periodicity
from .storage import HabitRepository


def get_all_habits(repo: HabitRepository) -> list[Habit]:
    """Return all habits."""
    return repo.list_habits()


def get_habits_by_periodicity(repo: HabitRepository, periodicity: Periodicity) -> list[Habit]:
    """Return habits that share one periodicity."""
    return repo.list_habits_by_periodicity(periodicity)


def longest_streak_for_habit(repo: HabitRepository, habit_id: int) -> int:
    """Return the longest run streak for one habit based on its period type."""
    habit = repo.get_habit_by_id(habit_id)
    completions = repo.list_completions(habit_id)
    return _longest_streak_from_datetimes(completions, habit.periodicity)


def longest_streak_of_all_habits(repo: HabitRepository) -> tuple[Habit | None, int]:
    """Return the habit with the longest streak and its streak size."""
    habits = repo.list_habits()
    scored = list(
        map(
            lambda habit: (habit, _longest_streak_from_datetimes(repo.list_completions(habit.id), habit.periodicity)),
            habits,
        )
    )
    if not scored:
        return None, 0
    return max(scored, key=lambda entry: entry[1])


def _period_key(value: datetime, periodicity: Periodicity) -> int:
    if periodicity == Periodicity.DAILY:
        return value.date().toordinal()
    iso_year, iso_week, _ = value.isocalendar()
    return iso_year * 100 + iso_week


def _longest_streak_from_datetimes(values: Iterable[datetime], periodicity: Periodicity) -> int:
    period_ids = sorted({_period_key(value, periodicity) for value in values})
    if not period_ids:
        return 0

    reducer = lambda acc, cur: (
        (cur, acc[1] + 1, max(acc[2], acc[1] + 1))
        if cur == acc[0] + 1
        else (cur, 1, max(acc[2], 1))
    )

    prev, current, best = period_ids[0], 1, 1
    for period_id in period_ids[1:]:
        prev, current, best = reducer((prev, current, best), period_id)
    return best
