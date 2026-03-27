# Habit Tracker (Python CLI Backend)

A practical, extensible habit tracking backend with persistence, analytics, and rich periodic scheduling.

## What’s new in this version

This version expands the app beyond the basic requirements and introduces:

- **Extended periodicity support**: `daily`, `weekly`, `monthly`, `yearly`, and `custom`.
- **Custom recurrence intervals** with `--interval-days` for flexible habits (e.g., every 10 days).
- **Configurable per-period targets** with `--target`.
- **New analytics**:
  - longest streak (per habit and globally)
  - current streak
  - trailing completion rate
  - next due date estimation
- **Expanded fixtures** including monthly/yearly/custom examples.
- **Stronger tests** for new periodicities and analytics.

---

## Requirements

- Python 3.8+

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install pytest
```

## Quick start

```bash
python -m habit_tracker.cli --db habits.db init-db
python -m habit_tracker.cli --db habits.db load-fixtures
python -m habit_tracker.cli --db habits.db list
python -m habit_tracker.cli --db habits.db by-period monthly
python -m habit_tracker.cli --db habits.db by-period yearly
python -m habit_tracker.cli --db habits.db by-period custom
python -m habit_tracker.cli --db habits.db longest-streak
```

---

## Command reference

### 1) Database and fixture management

```bash
python -m habit_tracker.cli --db habits.db init-db
python -m habit_tracker.cli --db habits.db load-fixtures
python -m habit_tracker.cli --db habits.db list
```

### 2) Habit lifecycle

Create habits across all periodicity types:

```bash
# Daily
python -m habit_tracker.cli --db habits.db create "Sleep" "Sleep 8 hours" daily

# Weekly
python -m habit_tracker.cli --db habits.db create "Workout" "Strength training" weekly

# Monthly
python -m habit_tracker.cli --db habits.db create "Budget Review" "Review budget performance" monthly

# Yearly
python -m habit_tracker.cli --db habits.db create "Tax Prep" "Prepare yearly tax package" yearly

# Custom periodicity every 10 days
python -m habit_tracker.cli --db habits.db create "Deep Clean" "Clean one room" custom --interval-days 10
```

Set higher completion targets per period:

```bash
python -m habit_tracker.cli --db habits.db create "Language Practice" "Practice vocabulary" daily --target 2
```

Delete and check off:

```bash
python -m habit_tracker.cli --db habits.db delete 2
python -m habit_tracker.cli --db habits.db checkoff 1
```

### 3) Filtering and analytics

```bash
python -m habit_tracker.cli --db habits.db by-period daily
python -m habit_tracker.cli --db habits.db by-period weekly
python -m habit_tracker.cli --db habits.db by-period monthly
python -m habit_tracker.cli --db habits.db by-period yearly
python -m habit_tracker.cli --db habits.db by-period custom

python -m habit_tracker.cli --db habits.db streak 1
python -m habit_tracker.cli --db habits.db current-streak 1
python -m habit_tracker.cli --db habits.db completion-rate 1 --periods 12
python -m habit_tracker.cli --db habits.db next-due 1
python -m habit_tracker.cli --db habits.db longest-streak
```

---

## Data model

Each habit now tracks:

- `id`
- `name`
- `description`
- `periodicity` (`daily`, `weekly`, `monthly`, `yearly`, `custom`)
- `interval_days` (used directly for custom periodicity, and defaults for standard types)
- `target_per_period`
- `created_at`

Completions are stored as timestamps (`completed_at`) linked to `habit_id`.

---

## Predefined fixture habits

`habit_tracker/fixtures.py` includes:

- Daily: Drink Water, Read, Meditate
- Weekly: Workout, Plan Week
- Monthly: Budget Review
- Yearly: Tax Prep
- Custom: Deep Clean (every 10 days)

The fixture dataset includes 4 weeks of dense data plus monthly/yearly/custom examples.

---

## Project structure

- `habit_tracker/models.py` — domain model, periodicity enum, default intervals.
- `habit_tracker/storage.py` — SQLite persistence and schema migration helpers.
- `habit_tracker/analytics.py` — streaks, completion rates, due date projections.
- `habit_tracker/fixtures.py` — predefined habits and fixture timeline.
- `habit_tracker/cli.py` — command-line API.
- `tests/test_habit_tracker.py` — unit tests for core and advanced behavior.
- `docs/user_guide.md` — detailed feature and usage documentation.

## Documentation

- `docs/user_guide.md` — full user/developer guide for all supported periodicities and analytics.
- `docs/conception_phase.md`
- `docs/development_phase_slides.md`
- `docs/final_abstract.md`

