# Habit Tracker (Python CLI Backend)

This project implements a basic habit tracking backend according to the portfolio acceptance criteria:
- Object-oriented domain model (`Habit` class).
- Daily and weekly habits.
- Habit check-off timestamps and creation timestamps.
- Persistent storage with SQLite.
- Functional analytics module.
- Command line API to create, delete, complete, and analyse habits.
- Unit tests for critical components.
- Predefined fixtures: 5 habits with 4 weeks of sample tracking data.

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
python -m habit_tracker.cli --db habits.db by-period daily
python -m habit_tracker.cli --db habits.db longest-streak
```

## CLI commands
```bash
python -m habit_tracker.cli --db habits.db create "Sleep" "Sleep 8 hours" daily
python -m habit_tracker.cli --db habits.db delete 2
python -m habit_tracker.cli --db habits.db checkoff 1
python -m habit_tracker.cli --db habits.db streak 1
```

## Predefined habits
`habit_tracker/fixtures.py` includes 5 predefined habits:
- 3 daily: Drink Water, Read, Meditate
- 2 weekly: Workout, Plan Week

The fixture generator creates 4 weeks of completion records for each predefined habit.

## Project structure
- `habit_tracker/models.py` — domain model and periodicity enum.
- `habit_tracker/storage.py` — SQLite persistence.
- `habit_tracker/analytics.py` — functional analytics functions.
- `habit_tracker/fixtures.py` — predefined habits and 4-week test fixture.
- `habit_tracker/cli.py` — CLI API.
- `tests/test_habit_tracker.py` — unit tests.

## Portfolio phase documents
- `docs/conception_phase.md` (1–3 page conceptual text + component diagram)
- `docs/development_phase_slides.md` (5–10 slide style content)
- `docs/final_abstract.md` (1–2 page abstract with making-of)

These Markdown documents can be exported to PDF for PebblePad submission.
