from habit_tracker import analytics
from habit_tracker.fixtures import PREDEFINED_HABITS, four_week_fixture
from habit_tracker.models import Periodicity
from habit_tracker.storage import HabitRepository


def test_create_and_list_habits(tmp_path):
    repo = HabitRepository(str(tmp_path / "test.db"))
    repo.initialize()
    repo.create_habit("Code", "Write Python code", Periodicity.DAILY)

    habits = repo.list_habits()

    assert len(habits) == 1
    assert habits[0].name == "Code"
    assert habits[0].periodicity == Periodicity.DAILY


def test_load_fixtures_and_filter_by_periodicity(tmp_path):
    repo = HabitRepository(str(tmp_path / "test.db"))
    repo.initialize()
    repo.load_fixture_data(PREDEFINED_HABITS, four_week_fixture())

    daily = analytics.get_habits_by_periodicity(repo, Periodicity.DAILY)
    weekly = analytics.get_habits_by_periodicity(repo, Periodicity.WEEKLY)

    assert len(daily) == 3
    assert len(weekly) == 2


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
