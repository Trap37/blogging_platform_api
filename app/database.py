from sqlmodel import Session, SQLModel, create_engine

from config import Config

config = Config()
connect_args = {'check_same_thread': False}
engine = create_engine(config.SQLALCHEMY_DATABASE_URI, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
