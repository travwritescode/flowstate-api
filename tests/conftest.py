import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from app.database import Base
import app.models.user  # noqa: F401 — registers User with Base.metadata
import app.models.task  # noqa: F401 — registers Task with Base.metadata


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )

    # SQLite does not enforce FK constraints by default — enable them explicitly
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(connection, _):
        connection.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)
