# HabitTracker User Guide

## 1) Purpose and scope

This guide documents how to install, run, and use the HabitTracker CLI backend.

HabitTracker provides:

- object-oriented habit modeling (`Habit` class),
- persistent storage with SQLite,
- completion tracking with timestamps,
- analytics functions (implemented in a functional style in the analytics module),
- and a command-line interface for CRUD + analysis operations.


## 2) Quick start

### 2.0 Prerequisites

Before installing or running HabitTracker, make sure you have:

- **Python 3.8+** (project metadata requires `>=3.8`)
- **pip** (for installing packages)
- **setuptools 61+** (required by the build system)
- **pytest** (required to run the automated test suite)

Optional but recommended:

- A virtual environment tool such as `venv`

### 2.1 Install

From the project root:

pip install -e .

### 2.2 Initialize a database

python -m habit_tracker.cli --db habits.db init-db

### 2.3 Load predefined habits + 4-week fixture data

python -m habit_tracker.cli --db habits.db load-fixtures

### 2.4 List habits

python -m habit_tracker.cli --db habits.db list


## 3) Command reference (all available commands + parameters)

Base command format:

python -m habit_tracker.cli [GLOBAL_OPTIONS] <COMMAND> [COMMAND_OPTIONS] [ARGS]

### 3.1 Global options

| Option | Type | Required | Default | Description |
|---|---|---:|---|---|
| `--db` | string (path) | No | `habits.db` | SQLite database file path. |


### 3.2 Commands

#### `init-db`
Initializes required SQLite tables.

python -m habit_tracker.cli --db habits.db init-db

Parameters: none.

#### `load-fixtures`
Initializes DB (if needed), then loads predefined habits and completion fixture data.

python -m habit_tracker.cli --db habits.db load-fixtures

Parameters: none.


#### `list`
Lists all tracked habits with metadata.

python -m habit_tracker.cli --db habits.db list

Parameters: none.


#### `create`
Creates a habit.

python -m habit_tracker.cli --db habits.db create "Read" "Read 20 minutes" daily
python -m habit_tracker.cli --db habits.db create "Deep Clean" "Every 10 days" custom --interval-days 10 --target 1

Positional arguments:

| Arg | Type | Required | Allowed values | Description |
|---|---|---:|---|---|
| `name` | string | Yes | any non-empty string | Habit name (must be unique). |
| `description` | string | Yes | any non-empty string | Habit description/task specification. |
| `periodicity` | enum | Yes | `daily`, `weekly`, `monthly`, `yearly`, `custom` | Habit period type. |

Options:

| Option | Type | Required | Default | Description |
|---|---|---:|---|---|
| `--interval-days` | integer > 0 | No | periodicity default (`1/7/30/365/1`) | Number of days per period. Especially useful for `custom`. |
| `--target` | integer > 0 | No | `1` | Required completions per period. |


#### `delete`
Deletes a habit by id.

python -m habit_tracker.cli --db habits.db delete 3

Positional arguments:

| Arg | Type | Required | Description |
|---|---|---:|---|
| `habit_id` | integer | Yes | Habit ID to delete. |


#### `checkoff`
Adds a completion timestamp for a habit.

python -m habit_tracker.cli --db habits.db checkoff 2

Positional arguments:

| Arg | Type | Required | Description |
|---|---|---:|---|
| `habit_id` | integer | Yes | Habit ID to mark completed now (UTC timestamp). |


#### `streak`
Returns the longest historical streak for one habit.

python -m habit_tracker.cli --db habits.db streak 2

Positional arguments:

| Arg | Type | Required | Description |
|---|---|---:|---|
| `habit_id` | integer | Yes | Habit ID to analyze. |


#### `current-streak`
Returns the currently active streak for one habit.

python -m habit_tracker.cli --db habits.db current-streak 2

Positional arguments:

| Arg | Type | Required | Description |
|---|---|---:|---|
| `habit_id` | integer | Yes | Habit ID to analyze. |


#### `next-due`
Estimates the next due datetime for one habit.

python -m habit_tracker.cli --db habits.db next-due 2

Positional arguments:

| Arg | Type | Required | Description |
|---|---|---:|---|
| `habit_id` | integer | Yes | Habit ID to analyze. |


#### `completion-rate`
Returns trailing completion rate for one habit.

python -m habit_tracker.cli --db habits.db completion-rate 2 --periods 12

Positional arguments:

| Arg | Type | Required | Description |
|---|---|---:|---|
| `habit_id` | integer | Yes | Habit ID to analyze. |

Options:

| Option | Type | Required | Default | Description |
|---|---|---:|---|---|
| `--periods` | integer > 0 | No | `12` | Number of trailing periods used for the rate calculation. |


#### `longest-streak`
Returns the best streak among all habits.

python -m habit_tracker.cli --db habits.db longest-streak

Parameters: none.


#### `by-period`
Lists habits filtered by periodicity.

python -m habit_tracker.cli --db habits.db by-period daily
python -m habit_tracker.cli --db habits.db by-period weekly

Positional arguments:

| Arg | Type | Required | Allowed values | Description |
|---|---|---:|---|---|
| `periodicity` | enum | Yes | `daily`, `weekly`, `monthly`, `yearly`, `custom` | Filter criterion. |


## 4) Analytics semantics

- **Longest streak (per habit):** max consecutive completed periods in that habit’s history.
- **Current streak:** consecutive completed periods ending at the latest completed period.
- **Longest streak (global):** best streak among all habits.
- **Completion rate:** completed periods / total periods in a trailing window.
- **Next due date:** based on the most recent completion and interval (or creation date if no completions).


## 5) Compliance

### 5.1 Functional requirements coverage

- Habit concept is modeled as a class (`Habit`).
- Multiple habits are supported.
- Habits support daily and weekly periodicities (plus monthly/yearly/custom extensions).
- Completions are tracked with timestamps.
- Persistence is handled with SQLite.
- CLI supports creating, deleting, listing, and analytics operations.
- Analytics required by assignment are supported:
  - list all habits,
  - list habits by periodicity,
  - longest streak across all habits,
  - longest streak for a specific habit.
- Predefined habits and fixture history are available through `load-fixtures`.

## 6) Testing

Run tests from the project root:

pytest

Recommended additional CLI sanity checks:

python -m habit_tracker.cli --db habits.db init-db
python -m habit_tracker.cli --db habits.db load-fixtures
python -m habit_tracker.cli --db habits.db list
python -m habit_tracker.cli --db habits.db longest-streak