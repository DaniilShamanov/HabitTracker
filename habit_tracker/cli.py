"""Command-line interface for the habit tracker."""

from __future__ import annotations

import argparse

from . import analytics
from .fixtures import PREDEFINED_HABITS, four_week_fixture
from .models import Periodicity
from .storage import HabitRepository


def build_parser() -> argparse.ArgumentParser:
    """Build and return the root parser."""
    parser = argparse.ArgumentParser(prog="habit-tracker", description="Habit tracking CLI backend")
    parser.add_argument("--db", default="habits.db", help="Path to SQLite database file")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init-db", help="Initialize database tables")
    sub.add_parser("load-fixtures", help="Load 5 predefined habits and 4-week sample data")
    sub.add_parser("list", help="List all habits")

    create_p = sub.add_parser("create", help="Create a new habit")
    create_p.add_argument("name")
    create_p.add_argument("description")
    create_p.add_argument("periodicity", choices=[p.value for p in Periodicity])

    delete_p = sub.add_parser("delete", help="Delete an existing habit")
    delete_p.add_argument("habit_id", type=int)

    checkoff_p = sub.add_parser("checkoff", help="Mark a habit task as completed")
    checkoff_p.add_argument("habit_id", type=int)

    streak_p = sub.add_parser("streak", help="Get longest streak for one habit")
    streak_p.add_argument("habit_id", type=int)

    all_streak = sub.add_parser("longest-streak", help="Get longest streak among all habits")
    all_streak.set_defaults()

    by_period = sub.add_parser("by-period", help="List habits by periodicity")
    by_period.add_argument("periodicity", choices=[p.value for p in Periodicity])

    return parser


def main() -> None:
    """CLI entrypoint."""
    args = build_parser().parse_args()
    repo = HabitRepository(args.db)

    if args.command == "init-db":
        repo.initialize()
        print("Database initialized")
    elif args.command == "load-fixtures":
        repo.initialize()
        repo.load_fixture_data(PREDEFINED_HABITS, four_week_fixture())
        print("Loaded predefined habits with 4-week fixture data")
    elif args.command == "list":
        for habit in analytics.get_all_habits(repo):
            print(f"{habit.id}: {habit.name} [{habit.periodicity.value}] created={habit.created_at.isoformat()}")
    elif args.command == "create":
        habit = repo.create_habit(args.name, args.description, Periodicity(args.periodicity))
        print(f"Created habit {habit.id}: {habit.name}")
    elif args.command == "delete":
        repo.delete_habit(args.habit_id)
        print(f"Deleted habit {args.habit_id}")
    elif args.command == "checkoff":
        repo.complete_habit(args.habit_id)
        print(f"Completed habit {args.habit_id}")
    elif args.command == "streak":
        value = analytics.longest_streak_for_habit(repo, args.habit_id)
        print(f"Longest streak for habit {args.habit_id}: {value}")
    elif args.command == "longest-streak":
        habit, streak = analytics.longest_streak_of_all_habits(repo)
        if habit is None:
            print("No habits found")
        else:
            print(f"Longest streak: {streak} ({habit.name})")
    elif args.command == "by-period":
        habits = analytics.get_habits_by_periodicity(repo, Periodicity(args.periodicity))
        for habit in habits:
            print(f"{habit.id}: {habit.name}")


if __name__ == "__main__":
    main()
