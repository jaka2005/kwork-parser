from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


Base = declarative_base()


class Projects(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, autoincrement=False)


def get_session(connection_url="sqlite:///database.db"):
    engine = create_engine(connection_url)
    session = Session(engine)
    Base.metadata.create_all(engine)

    return session
