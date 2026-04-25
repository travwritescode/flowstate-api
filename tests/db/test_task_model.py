import time

import pytest
from sqlalchemy.exc import IntegrityError

from app.models.task import Task, TaskPriority, TaskStatus
from app.models.user import User


@pytest.fixture
def user(db):
    u = User(email="owner@example.com", hashed_password="hashed")
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


class TestCreateTask:
    def test_task_is_inserted(self, db, user):
        task = Task(title="Write tests", owner_id=user.id)
        db.add(task)
        db.commit()
        db.refresh(task)

        assert task.id is not None
        assert task.title == "Write tests"

    def test_task_can_be_queried_back(self, db, user):
        task = Task(title="Write tests", owner_id=user.id)
        db.add(task)
        db.commit()

        fetched = db.query(Task).filter(Task.id == task.id).first()
        assert fetched is not None
        assert fetched.title == "Write tests"


class TestTaskDefaults:
    def test_status_defaults_to_todo(self, db, user):
        task = Task(title="Write tests", owner_id=user.id)
        db.add(task)
        db.commit()
        db.refresh(task)

        assert task.status == TaskStatus.todo

    def test_priority_defaults_to_medium(self, db, user):
        task = Task(title="Write tests", owner_id=user.id)
        db.add(task)
        db.commit()
        db.refresh(task)

        assert task.priority == TaskPriority.medium

    def test_is_deleted_defaults_to_false(self, db, user):
        task = Task(title="Write tests", owner_id=user.id)
        db.add(task)
        db.commit()
        db.refresh(task)

        assert task.is_deleted is False

    def test_created_at_is_populated(self, db, user):
        task = Task(title="Write tests", owner_id=user.id)
        db.add(task)
        db.commit()
        db.refresh(task)

        assert task.created_at is not None

    def test_updated_at_is_populated(self, db, user):
        task = Task(title="Write tests", owner_id=user.id)
        db.add(task)
        db.commit()
        db.refresh(task)

        assert task.updated_at is not None


class TestTaskConstraints:
    def test_invalid_owner_id_raises_integrity_error(self, db):
        task = Task(title="Orphan task", owner_id=99999)
        db.add(task)
        with pytest.raises(IntegrityError):
            db.commit()

    def test_title_is_required(self, db, user):
        task = Task(owner_id=user.id)
        db.add(task)
        with pytest.raises(IntegrityError):
            db.commit()


class TestSoftDelete:
    def test_soft_deleted_row_still_exists(self, db, user):
        task = Task(title="To be deleted", owner_id=user.id)
        db.add(task)
        db.commit()
        db.refresh(task)
        task_id = task.id

        task.is_deleted = True
        db.commit()

        row = db.query(Task).filter(Task.id == task_id).first()
        assert row is not None
        assert row.is_deleted is True

    def test_soft_delete_does_not_reduce_row_count(self, db, user):
        task = Task(title="To be deleted", owner_id=user.id)
        db.add(task)
        db.commit()

        count_before = db.query(Task).count()
        task.is_deleted = True
        db.commit()
        count_after = db.query(Task).count()

        assert count_after == count_before


class TestUpdatedAt:
    def test_updated_at_changes_after_update(self, db, user):
        task = Task(title="Original title", owner_id=user.id)
        db.add(task)
        db.commit()
        db.refresh(task)
        original_updated_at = task.updated_at

        # small sleep so the timestamp has time to change
        time.sleep(1)

        task.title = "Updated title"
        db.commit()
        db.refresh(task)

        assert task.updated_at > original_updated_at
