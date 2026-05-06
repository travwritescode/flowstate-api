from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, EmailStr, model_validator

from app.models.user import User


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}

    @model_validator(mode="before")
    @classmethod
    def coerce_user(cls, data: Any) -> Any:
        if isinstance(data, User):
            return {
                "id": UUID(data.public_id),
                "email": data.email,
                "is_active": data.is_active,
                "created_at": data.created_at,
            }
        return data
