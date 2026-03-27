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


DEFAULT_INTERVAL_DAYS = {
        Periodicity.DAILY: 1,
        Periodicity.WEEKLY: 7,
        Periodicity.MONTHLY: 30,      # approximate
        Periodicity.YEARLY: 365,      # approximate
        Periodicity.CUSTOM: 1,        # fallback, but should be set explicitly
    }
