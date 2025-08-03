import os

import json
from pydantic import BaseModel, ConfigDict, Field, field_serializer
from pydantic.alias_generators import to_camel
from datetime import datetime

from config import BASEDIR


class Database:
    data: dict[int, 'PostModel']
    POSTS_DIR = f'{BASEDIR}/posts.json'

    def __init__(self):
        if not os.path.exists(self.POSTS_DIR):
            os.makedirs(self.POSTS_DIR)

        try:
            with open(self.POSTS_DIR, 'r') as f:
                self.data = {
                    id: PostModel.model_construct(data)
                    for id, data in json.load(f).items()
                }
        except json.JSONDecodeError as e:
            raise Exception(
                f'Json decode error in posts dir. You must correct the json before loading the database. Path: "{self.POSTS_DIR}"'
            ) from e

    def save(self):
        try:
            with open(self.POSTS_DIR, 'w') as f:
                self.data = json.dump(self.data, f)
        except json.JSONDecodeError as e:
            raise Exception(
                f'Json decode error in posts dir. You must correct the json before loading the database. Path: "{self.POSTS_DIR}"'
            ) from e

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name == 'data':
            self.save()

    # FEATURE: Maybe add a cache here or something?
    # Could add a second dict to the database with the validated models in them and check
    # if they were already loaded. Might be a waste because model_construct is already so fast
    def get(self, id: int) -> 'PostModel':
        return PostModel.model_construct(*self.data[id])


# TODO: Should create enum of all options for tags and categories
class PostCreate(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    title: str
    content: str
    category: str
    tags: list[str] = []

    # TODO: Should use model_construct here instead for better performance
    # This data is already validated so no need to revalidate
    def to_model(self, id: int):
        return PostModel.model_construct(
            id=id,
            title=self.title,
            content=self.content,
            category=self.category,
            tags=self.tags,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )


# NOTE: Do not instantiate this directly
# TODO: Maybe use strings instead of datetime classes?
class PostModel(PostCreate):
    id: int
    created_at: datetime = Field(datetime.now())
    updated_at: datetime = Field(datetime.now())

    @field_serializer('created_at', 'updated_at')
    def date_to_string(self, date: datetime) -> str:
        return date.strftime('%Y-%m-%dT%H:%M:%SZ')

    def __setattr__(self, name, value):
        if name not in {'updated_at', 'created_at'} and hasattr(self, name):
            super().__setattr__('updated_at', datetime.now())
        super().__setattr__(name, value)

    def to_json(self):
        return self.model_dump_json(by_alias=True)
