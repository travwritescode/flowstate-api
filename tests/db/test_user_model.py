import pytest
from sqlalchemy.exc import IntegrityError

from app.models.user import User


class TestCreateUser:
    def test_user_is_inserted(self, db):
        user = User(email="test@example.com", hashed_password="hashed")
        db.add(user)
        db.commit()
        db.refresh(user)

        assert user.id is not None
        assert user.public_id is not None
        assert len(user.public_id) == 36
        assert user.email == "test@example.com"

    def test_user_can_be_queried_back(self, db):
        user = User(email="test@example.com", hashed_password="hashed")
        db.add(user)
        db.commit()

        fetched = db.query(User).filter(User.email == "test@example.com").first()
        assert fetched is not None
        assert fetched.id == user.id


class TestUserDefaults:
    def test_is_active_defaults_to_true(self, db):
        user = User(email="test@example.com", hashed_password="hashed")
        db.add(user)
        db.commit()
        db.refresh(user)

        assert user.is_active is True

    def test_created_at_is_populated(self, db):
        user = User(email="test@example.com", hashed_password="hashed")
        db.add(user)
        db.commit()
        db.refresh(user)

        assert user.created_at is not None


class TestUserConstraints:
    def test_duplicate_email_raises_integrity_error(self, db):
        user1 = User(email="dupe@example.com", hashed_password="hashed")
        db.add(user1)
        db.commit()

        user2 = User(email="dupe@example.com", hashed_password="hashed")
        db.add(user2)
        with pytest.raises(IntegrityError):
            db.commit()

    def test_email_is_required(self, db):
        user = User(hashed_password="hashed")
        db.add(user)
        with pytest.raises(IntegrityError):
            db.commit()

    def test_hashed_password_is_required(self, db):
        user = User(email="test@example.com")
        db.add(user)
        with pytest.raises(IntegrityError):
            db.commit()
