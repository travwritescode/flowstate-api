import pytest

from app.models.task import TaskPriority, TaskStatus


class TestTaskStatus:
    def test_all_members_are_strings(self):
        for member in TaskStatus:
            assert isinstance(member, str)

    def test_todo_value(self):
        assert TaskStatus.todo == "todo"

    def test_in_progress_value(self):
        assert TaskStatus.in_progress == "in_progress"

    def test_done_value(self):
        assert TaskStatus.done == "done"

    def test_member_count(self):
        assert len(TaskStatus) == 3

    def test_invalid_value_raises(self):
        with pytest.raises(ValueError):
            TaskStatus("invalid_status")


class TestTaskPriority:
    def test_all_members_are_strings(self):
        for member in TaskPriority:
            assert isinstance(member, str)

    def test_low_value(self):
        assert TaskPriority.low == "low"

    def test_medium_value(self):
        assert TaskPriority.medium == "medium"

    def test_high_value(self):
        assert TaskPriority.high == "high"

    def test_member_count(self):
        assert len(TaskPriority) == 3

    def test_invalid_value_raises(self):
        with pytest.raises(ValueError):
            TaskPriority("urgent")
