from fastapi import FastAPI, HTTPException, status

from app.models import Database, PostCreate, PostModel

app = FastAPI()
database = Database()

# posts = {
#     0: PostModel.model_validate(
#         {
#             'id': 0,
#             'title': 'My First Blog Post',
#             'content': 'This is the content of my first blog post.',
#             'category': 'Technology',
#             'tags': ['Tech', 'Programming'],
#             'createdAt': '2021-09-01T12:00:00Z',
#             'updatedAt': '2021-09-01T12:00:00Z',
#         }
#     ),
#     1: PostModel.model_validate(
#         {
#             'id': 1,
#             'title': 'My Second Blog Post',
#             'content': 'This is the content of my second blog post.',
#             'category': 'Music',
#             'tags': ['TAG1', 'TAG2'],
#             'createdAt': '2021-09-01T12:00:00Z',
#             'updatedAt': '2021-09-01T12:00:00Z',
#         }
#     ),
#     2: PostModel.model_validate(
#         {
#             'id': 2,
#             'title': 'My Second Blog Post',
#             'content': 'This is the content of my second blog post.',
#             'category': 'Math',
#             'tags': ['Blah', 'YUR'],
#             'createdAt': '2021-09-01T12:00:00Z',
#             'updatedAt': '2021-09-01T12:00:00Z',
#         }
#     ),
# }


# TODO: Can add 400 error for missing fields
# "message": f"Missing required fields: {', '.join(missing_fields)}",
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate) -> PostModel:
    id = len(database.data) + 1

    post = post.to_model(id)
    database.data[id] = post

    return post


@app.get('/posts/{post_id}')
def get_post(post_id: int) -> PostModel:
    if post_id not in posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Item not found'
        )
    return posts[post_id]
