"""Domain models for the habit tracker."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Periodicity(str, Enum):
    """Supported habit periodicities."""

    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    CUSTOM = "custom"


DEFAULT_INTERVAL_DAYS: dict[Periodicity, int] = {
    Periodicity.DAILY: 1,
    Periodicity.WEEKLY: 7,
    Periodicity.MONTHLY: 30,
    Periodicity.YEARLY: 365,
    Periodicity.CUSTOM: 1,
}


@dataclass(frozen=True)
class Habit:
    """Represents a user-defined habit and its metadata."""

    id: int
    name: str
    description: str
    periodicity: Periodicity
    interval_days: int
    target_per_period: int
    created_at: datetime
