# HabitTracker User Guide

## Overview

HabitTracker is a CLI-first habit tracking backend that combines:

- persistent SQLite storage,
- flexible periodic scheduling,
- streak analytics,
- and reproducible fixture data for demos/tests.

## Periodicity system

HabitTracker supports five periodicity modes:

1. **daily**: one period per calendar day
2. **weekly**: one period per ISO week
3. **monthly**: one period per calendar month
4. **yearly**: one period per calendar year
5. **custom**: one period per `interval_days`

### Interval behavior

- Daily defaults to interval `1`
- Weekly defaults to interval `7`
- Monthly defaults to interval `30`
- Yearly defaults to interval `365`
- Custom defaults to `1`, but you typically set it explicitly

Example: `custom --interval-days 10` means every tenth day.

## CLI workflow

### Initialize database

```bash
python -m habit_tracker.cli --db habits.db init-db
```

### Seed example data

```bash
python -m habit_tracker.cli --db habits.db load-fixtures
```

### Create habits

```bash
python -m habit_tracker.cli --db habits.db create "Read" "Read 20 minutes" daily
python -m habit_tracker.cli --db habits.db create "Workout" "2 sessions/week" weekly
python -m habit_tracker.cli --db habits.db create "Budget" "Monthly budget review" monthly
python -m habit_tracker.cli --db habits.db create "Taxes" "Annual tax prep" yearly
python -m habit_tracker.cli --db habits.db create "Deep Clean" "Every 10 days" custom --interval-days 10
```

### Check off a completion

```bash
python -m habit_tracker.cli --db habits.db checkoff 1
```

### Analytics

```bash
python -m habit_tracker.cli --db habits.db streak 1
python -m habit_tracker.cli --db habits.db current-streak 1
python -m habit_tracker.cli --db habits.db completion-rate 1 --periods 12
python -m habit_tracker.cli --db habits.db next-due 1
python -m habit_tracker.cli --db habits.db longest-streak
```

## Analytics semantics

- **Longest streak**: max consecutive completed periods in history.
- **Current streak**: consecutive completed periods ending at latest completed period.
- **Completion rate**: ratio of completed periods in trailing `N` periods.
- **Next due date**: latest completion plus interval (or creation date if none completed).

## Database notes

Schema includes migration-safe column bootstrapping for:

- `interval_days`
- `target_per_period`

This lets older local DB files be upgraded without dropping data.

## Testing

Run:

```bash
pytest
```

The suite validates:

- CRUD basics,
- periodicity filtering,
- streak computations,
- monthly/yearly/custom behavior,
- due date and completion-rate helpers.
