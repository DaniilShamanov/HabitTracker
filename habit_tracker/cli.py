"""Command-line interface for the habit tracker."""

from __future__ import annotations

import argparse

from . import analytics
from .fixtures import PREDEFINED_HABITS, four_week_fixture
from .models import Periodicity
from .storage import HabitAlreadyExistsError, HabitRepository


def build_parser() -> argparse.ArgumentParser:
    """Build and return the root parser."""
    parser = argparse.ArgumentParser(prog="habit-tracker", description="Habit tracking CLI backend")
    parser.add_argument("--db", default="habits.db", help="Path to SQLite database file")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init-db", help="Initialize database tables")
    sub.add_parser("load-fixtures", help="Load predefined habits and sample data")
    sub.add_parser("list", help="List all habits")

    create_p = sub.add_parser("create", help="Create a new habit")
    create_p.add_argument("name")
    create_p.add_argument("description")
    create_p.add_argument("periodicity", choices=[p.value for p in Periodicity])
    create_p.add_argument("--interval-days", type=int, default=None, help="Custom number of days between due periods")
    create_p.add_argument("--target", type=int, default=1, help="How many completions are required per period")

    delete_p = sub.add_parser("delete", help="Delete an existing habit")
    delete_p.add_argument("habit_id", type=int)

    checkoff_p = sub.add_parser("checkoff", help="Mark a habit task as completed")
    checkoff_p.add_argument("habit_id", type=int)

    streak_p = sub.add_parser("streak", help="Get longest streak for one habit")
    streak_p.add_argument("habit_id", type=int)

    current_streak_p = sub.add_parser("current-streak", help="Get active streak for one habit")
    current_streak_p.add_argument("habit_id", type=int)

    due_p = sub.add_parser("next-due", help="Estimate next due date for one habit")
    due_p.add_argument("habit_id", type=int)

    rate_p = sub.add_parser("completion-rate", help="Get trailing completion rate for one habit")
    rate_p.add_argument("habit_id", type=int)
    rate_p.add_argument("--periods", type=int, default=12)

    sub.add_parser("longest-streak", help="Get longest streak among all habits")

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
        print("Loaded predefined habits with fixture data")
    elif args.command == "list":
        for habit in analytics.get_all_habits(repo):
            print(
                f"{habit.id}: {habit.name} [{habit.periodicity.value}] "
                f"every {habit.interval_days} day(s), target={habit.target_per_period}, "
                f"created={habit.created_at.isoformat()}"
            )
    elif args.command == "create":
        try:
            habit = repo.create_habit(args.name, args.description, Periodicity(args.periodicity))
            print(f"Created habit {habit.id}: {habit.name}")
        except HabitAlreadyExistsError as exc:
            raise SystemExit(str(exc))
    elif args.command == "delete":
        repo.delete_habit(args.habit_id)
        print(f"Deleted habit {args.habit_id}")
    elif args.command == "checkoff":
        repo.complete_habit(args.habit_id)
        print(f"Completed habit {args.habit_id}")
    elif args.command == "streak":
        value = analytics.longest_streak_for_habit(repo, args.habit_id)
        print(f"Longest streak for habit {args.habit_id}: {value}")
    elif args.command == "current-streak":
        value = analytics.current_streak_for_habit(repo, args.habit_id)
        print(f"Current streak for habit {args.habit_id}: {value}")
    elif args.command == "next-due":
        value = analytics.next_due_date(repo, args.habit_id)
        print(f"Next due for habit {args.habit_id}: {value.isoformat()}")
    elif args.command == "completion-rate":
        value = analytics.completion_rate(repo, args.habit_id, args.periods)
        print(f"Completion rate for habit {args.habit_id}: {value:.2%}")
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
