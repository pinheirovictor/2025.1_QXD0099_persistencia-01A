from sqlmodel import SQLModel, create_engine, Session

from sqlmodel import Session, create_engine
engine = create_engine("sqlite:///marketplace.db")


def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
