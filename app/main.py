from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import create_db_and_tables
from app.routes import router as post_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Before yield in on startup and after in on exit
    # TODO: For production you would probably use a migration script
    # that runs before you start your app. (SQLModel will have migration
    # utilities wrapping Alembic, but for now, you can use Alembic directly.)
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(post_router)
