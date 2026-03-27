"""Functional analytics utilities for habit data."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Iterable

from .models import Habit, Periodicity
from .storage import HabitRepository


_EPOCH = datetime(1970, 1, 1, tzinfo=UTC)


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
    return _longest_streak_from_datetimes(completions, habit)


def current_streak_for_habit(repo: HabitRepository, habit_id: int) -> int:
    """Return the active streak from the most recent completion period backwards."""
    habit = repo.get_habit_by_id(habit_id)
    period_ids = sorted({_period_key(value, habit) for value in repo.list_completions(habit_id)})
    if not period_ids:
        return 0

    streak = 1
    prev = period_ids[-1]
    for cur in reversed(period_ids[:-1]):
        if cur == prev - 1:
            streak += 1
            prev = cur
        else:
            break
    return streak


def completion_rate(repo: HabitRepository, habit_id: int, periods: int = 12) -> float:
    """Return completion rate as completed periods / observed periods over trailing window."""
    habit = repo.get_habit_by_id(habit_id)
    period_ids = sorted({_period_key(value, habit) for value in repo.list_completions(habit_id)})
    if not period_ids:
        return 0.0
    latest = period_ids[-1]
    earliest = max(period_ids[0], latest - periods + 1)
    expected = latest - earliest + 1
    completed = len([pid for pid in period_ids if earliest <= pid <= latest])
    return completed / expected if expected else 0.0


def next_due_date(repo: HabitRepository, habit_id: int) -> datetime:
    """Estimate the next due date based on the latest completion and interval configuration."""
    habit = repo.get_habit_by_id(habit_id)
    completions = repo.list_completions(habit_id)
    pivot = completions[-1] if completions else habit.created_at
    return pivot + timedelta(days=habit.interval_days)


def longest_streak_of_all_habits(repo: HabitRepository) -> tuple[Habit | None, int]:
    """Return the habit with the longest streak and its streak size."""
    habits = repo.list_habits()
    scored = [(habit, _longest_streak_from_datetimes(repo.list_completions(habit.id), habit)) for habit in habits]
    if not scored:
        return None, 0
    return max(scored, key=lambda entry: entry[1])


def _period_key(value: datetime, habit: Habit) -> int:
    moment = value if value.tzinfo else value.replace(tzinfo=UTC)
    if habit.periodicity == Periodicity.DAILY:
        return moment.date().toordinal()
    if habit.periodicity == Periodicity.WEEKLY:
        iso_year, iso_week, _ = moment.isocalendar()
        return iso_year * 53 + iso_week
    if habit.periodicity == Periodicity.MONTHLY:
        return moment.year * 12 + moment.month
    if habit.periodicity == Periodicity.YEARLY:
        return moment.year
    return (moment - _EPOCH).days // habit.interval_days


def _longest_streak_from_datetimes(values: Iterable[datetime], habit: Habit) -> int:
    period_ids = sorted({_period_key(value, habit) for value in values})
    if not period_ids:
        return 0

    prev, current, best = period_ids[0], 1, 1
    for period_id in period_ids[1:]:
        if period_id == prev + 1:
            current += 1
        else:
            current = 1
        best = max(best, current)
        prev = period_id
    return best
