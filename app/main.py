from fastapi import FastAPI
from pydantic import BaseModel, Field, field_serializer

from datetime import datetime

app = FastAPI()


# TODO: Add defaults to created_at and updated_at
class PostModel(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: list[str] = []
    created_at: datetime = Field(datetime.now(), alias='createdAt')
    updated_at: datetime = Field(datetime.now(), alias='updatedAt')

    @field_serializer('created_at', 'updated_at')
    def date_to_string(self, date: datetime) -> str:
        return date.strftime('%Y-%m-%dT%H:%M:%SZ')

    def to_json(self):
        return self.model_dump_json(by_alias=True)


posts = {
    0: PostModel.model_validate(
        {
            'id': 0,
            'title': 'My First Blog Post',
            'content': 'This is the content of my first blog post.',
            'category': 'Technology',
            'tags': ['Tech', 'Programming'],
            'createdAt': '2021-09-01T12:00:00Z',
            'updatedAt': '2021-09-01T12:00:00Z',
        }
    ),
    1: PostModel.model_validate(
        {
            'id': 1,
            'title': 'My Second Blog Post',
            'content': 'This is the content of my second blog post.',
            'category': 'Music',
            'tags': ['TAG1', 'TAG2'],
            'createdAt': '2021-09-01T12:00:00Z',
            'updatedAt': '2021-09-01T12:00:00Z',
        }
    ),
    2: PostModel.model_validate(
        {
            'id': 2,
            'title': 'My Second Blog Post',
            'content': 'This is the content of my second blog post.',
            'category': 'Math',
            'tags': ['Blah', 'YUR'],
            'createdAt': '2021-09-01T12:00:00Z',
            'updatedAt': '2021-09-01T12:00:00Z',
        }
    ),
}
print(posts[0].to_json())


@app.get('/posts/{post_id}')
def get_post(post_id: int): ...
