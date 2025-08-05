from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from app.database import get_session
from app.models import (
    FilterParams,
    PostCreate,
    PostPrivate,
    PostPublic,
    PostUpdate,
)

router = APIRouter(prefix='/posts', tags=['Posts'])


SessionDep = Annotated[Session, Depends(get_session)]
FilterQuery = Annotated[FilterParams, Query()]


@router.post('/posts', response_model=PostPublic, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, session: SessionDep):
    db_post = PostPrivate.model_validate(post)

    session.add(db_post)
    session.commit()
    session.refresh(db_post)

    return db_post


# FEATURE: Maybe a better way to do the filtering
@router.get('/posts', response_model=list[PostPublic], status_code=status.HTTP_200_OK)
def get_posts(filter_query: FilterQuery, session: SessionDep):
    search_filter = f'%{filter_query.filter}%'
    posts = session.exec(
        select(PostPrivate).filter(
            PostPrivate.title.ilike(search_filter),  # type:ignore
            PostPrivate.category.ilike(search_filter),  # type:ignore
            PostPrivate.tags.ilike(search_filter),  # type:ignore
        )
    ).all()
    return posts


@router.get(
    '/posts/{post_id}', response_model=list[PostPublic], status_code=status.HTTP_200_OK
)
def get_post(post_id: int, session: SessionDep):
    post = session.get(PostPrivate, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Post not found'
        )

    return post


@router.patch(
    '/posts/{post_id}', response_model=PostPublic, status_code=status.HTTP_200_OK
)
def update_post(post_id: int, post: PostUpdate, session: SessionDep):
    post_db = session.get(PostPrivate, post_id)
    if not post_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Post not found'
        )

    if post_data := post.model_dump(exclude_unset=True):
        post_db.sqlmodel_update(post_data)
        # TODO: Add automated updates of post updated_at attr with SQLAlchemy events
        post_db.updated_at = datetime.now(timezone.utc)

    session.add(post_db)
    session.commit()
    session.refresh(post_db)

    return post_db


@router.delete('/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, session: SessionDep):
    post = session.get(PostPrivate, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Post not found'
        )

    session.delete(post)
    session.commit()
