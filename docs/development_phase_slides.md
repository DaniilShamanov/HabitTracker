# Development/Reflection Phase — Slide Content

## Slide 1 — Product Overview
Habit Tracker backend for daily/weekly habit management with CLI and analytics.

## Slide 2 — Technology Choices
- Python 3.8+
- sqlite3 for persistence
- argparse for CLI
- pytest for tests

## Slide 3 — Domain Design
- `Habit` class (OOP)
- `Periodicity` enum (daily, weekly)
- Datetime-based completion records

## Slide 4 — Persistence
- Table `habits`
- Table `completions`
- Foreign key relation and cascading delete

## Slide 5 — CLI API
- `init-db`, `load-fixtures`, `list`
- `create`, `delete`, `checkoff`
- `streak`, `longest-streak`, `by-period`

## Slide 6 — Analytics (Functional)
- list all habits
- list by periodicity
- longest streak per habit
- longest streak globally

## Slide 7 — Fixtures
- 5 predefined habits
- 4 weeks of completion history per habit
- Supports reproducible testing and demos

## Slide 8 — Testing
- CRUD and listing test
- periodicity filtering test
- streak correctness tests

## Slide 9 — Reflection
What went well: clear layering, deterministic fixtures, simple CLI UX.
Challenges: weekly streak keying and edge-case handling for missing periods.

## Slide 10 — Next Steps
- Multi-user support
- Richer analytics (current streak, missed periods)
- Optional GUI/web frontend
