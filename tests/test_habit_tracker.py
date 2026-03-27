import pytest

from habit_tracker import analytics
from habit_tracker.fixtures import PREDEFINED_HABITS, four_week_fixture
from habit_tracker.models import Periodicity
from habit_tracker.storage import HabitAlreadyExistsError, HabitRepository


def test_create_and_list_habits(tmp_path):
    repo = HabitRepository(str(tmp_path / "test.db"))
    repo.initialize()
    repo.create_habit("Code", "Write Python code", Periodicity.DAILY)

    habits = repo.list_habits()

    assert len(habits) == 1
    assert habits[0].name == "Code"
    assert habits[0].periodicity == Periodicity.DAILY
    assert habits[0].interval_days == 1


def test_load_fixtures_and_filter_by_periodicity(tmp_path):
    repo = HabitRepository(str(tmp_path / "test.db"))
    repo.initialize()
    repo.load_fixture_data(PREDEFINED_HABITS, four_week_fixture())

    daily = analytics.get_habits_by_periodicity(repo, Periodicity.DAILY)
    weekly = analytics.get_habits_by_periodicity(repo, Periodicity.WEEKLY)
    monthly = analytics.get_habits_by_periodicity(repo, Periodicity.MONTHLY)
    yearly = analytics.get_habits_by_periodicity(repo, Periodicity.YEARLY)
    custom = analytics.get_habits_by_periodicity(repo, Periodicity.CUSTOM)

    assert len(daily) == 3
    assert len(weekly) == 2


def test_create_duplicate_habit_name_raises_friendly_error(tmp_path):
    repo = HabitRepository(str(tmp_path / "test.db"))
    repo.initialize()
    repo.create_habit("Workout", "2 sessions/week", Periodicity.WEEKLY)

    with pytest.raises(HabitAlreadyExistsError):
        repo.create_habit("Workout", "Duplicate", Periodicity.WEEKLY)


def test_longest_streak_for_single_habit(tmp_path):
    repo = HabitRepository(str(tmp_path / "test.db"))
    repo.initialize()
    repo.load_fixture_data(PREDEFINED_HABITS, four_week_fixture())

    drink_water = next(h for h in repo.list_habits() if h.name == "Drink Water")
    streak = analytics.longest_streak_for_habit(repo, drink_water.id)

    assert streak == 28


def test_longest_streak_across_all_habits(tmp_path):
    repo = HabitRepository(str(tmp_path / "test.db"))
    repo.initialize()
    repo.load_fixture_data(PREDEFINED_HABITS, four_week_fixture())

    habit, streak = analytics.longest_streak_of_all_habits(repo)

    assert habit is not None
    assert habit.name == "Drink Water"
    assert streak == 28


def test_custom_periodicity_streak_and_next_due_date(tmp_path):
    repo = HabitRepository(str(tmp_path / "test.db"))
    repo.initialize()
    habit = repo.create_habit("Language", "Practice vocabulary", Periodicity.CUSTOM, interval_days=10)
    base = datetime(2026, 1, 1, 9, 0, 0, tzinfo=UTC)
    for day in (0, 10, 20):
        repo.complete_habit(habit.id, base + timedelta(days=day))

    assert analytics.longest_streak_for_habit(repo, habit.id) == 3
    assert analytics.current_streak_for_habit(repo, habit.id) == 3
    assert analytics.next_due_date(repo, habit.id) == base + timedelta(days=30)


def test_monthly_and_yearly_streaks(tmp_path):
    repo = HabitRepository(str(tmp_path / "test.db"))
    repo.initialize()
    monthly = repo.create_habit("Budget", "Monthly review", Periodicity.MONTHLY)
    yearly = repo.create_habit("Taxes", "Yearly paperwork", Periodicity.YEARLY)

    for dt in [datetime(2025, 11, 1), datetime(2025, 12, 1), datetime(2026, 1, 1)]:
        repo.complete_habit(monthly.id, dt)

    for dt in [datetime(2024, 4, 10), datetime(2025, 4, 10), datetime(2026, 4, 10)]:
        repo.complete_habit(yearly.id, dt)

    assert analytics.longest_streak_for_habit(repo, monthly.id) == 3
    assert analytics.longest_streak_for_habit(repo, yearly.id) == 3


def test_completion_rate(tmp_path):
    repo = HabitRepository(str(tmp_path / "test.db"))
    repo.initialize()
    habit = repo.create_habit("Reading", "Read daily", Periodicity.DAILY)

    start = datetime(2026, 1, 1)
    for day in [0, 1, 3, 4, 5]:
        repo.complete_habit(habit.id, start + timedelta(days=day))

    rate = analytics.completion_rate(repo, habit.id, periods=6)
    assert round(rate, 3) == round(5 / 6, 3)
