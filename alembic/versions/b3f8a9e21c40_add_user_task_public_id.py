"""add user and task public_id

Revision ID: b3f8a9e21c40
Revises: d40719549c6c
Create Date: 2026-05-06

"""
from __future__ import annotations

import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b3f8a9e21c40"
down_revision: Union[str, Sequence[str], None] = "d40719549c6c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("public_id", sa.String(length=36), nullable=True),
    )
    op.add_column(
        "tasks",
        sa.Column("public_id", sa.String(length=36), nullable=True),
    )

    conn = op.get_bind()
    users = conn.execute(sa.text("SELECT id FROM users")).all()
    for (user_id,) in users:
        conn.execute(
            sa.text("UPDATE users SET public_id = :pid WHERE id = :id"),
            {"pid": str(uuid.uuid4()), "id": user_id},
        )

    tasks = conn.execute(sa.text("SELECT id FROM tasks")).all()
    for (task_id,) in tasks:
        conn.execute(
            sa.text("UPDATE tasks SET public_id = :pid WHERE id = :id"),
            {"pid": str(uuid.uuid4()), "id": task_id},
        )

    op.create_index(
        op.f("ix_users_public_id"),
        "users",
        ["public_id"],
        unique=True,
    )
    op.create_index(
        op.f("ix_tasks_public_id"),
        "tasks",
        ["public_id"],
        unique=True,
    )

    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column(
            "public_id",
            existing_type=sa.String(length=36),
            nullable=False,
        )

    with op.batch_alter_table("tasks") as batch_op:
        batch_op.alter_column(
            "public_id",
            existing_type=sa.String(length=36),
            nullable=False,
        )


def downgrade() -> None:
    op.drop_index(op.f("ix_tasks_public_id"), table_name="tasks")
    op.drop_index(op.f("ix_users_public_id"), table_name="users")
    op.drop_column("tasks", "public_id")
    op.drop_column("users", "public_id")
