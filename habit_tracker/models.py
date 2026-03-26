"""Domain models for the habit tracker."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Periodicity(str, Enum):
    """Supported habit periodicities."""

    DAILY = "daily"
    WEEKLY = "weekly"


@dataclass(frozen=True)
class Habit:
    """Represents a user-defined habit and its metadata."""

    id: int
    name: str
    description: str
    periodicity: Periodicity
    created_at: datetime
