from datetime import datetime, timezone
from typing import Annotated

from fastapi import Query
from pydantic import BaseModel
from sqlmodel import JSON, Field, SQLModel


class FilterParams(BaseModel):
    filter: str = ''


FilterQuery = Annotated[FilterParams, Query()]


class PostBase(SQLModel):
    title: str = Field(index=True)
    content: str = Field()
    category: str = Field(index=True)
    tags: list[str] = Field(index=True, sa_type=JSON)


class PostPrivate(PostBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.now(timezone.utc))
    updated_at: datetime = Field(default=datetime.now(timezone.utc))


class PostPublic(PostBase):
    id: int = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()


class PostCreate(PostBase): ...


class PostUpdate(SQLModel):
    title: str | None = Field(default=None)
    content: str | None = Field(default=None)
    category: str | None = Field(default=None)
    tags: list[str] = Field(default_factory=list, sa_type=JSON)
