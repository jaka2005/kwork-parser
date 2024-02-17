from sqlite3 import IntegrityError
from typing import List, Self
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from config import DB_CONNECTION_URL


Base = declarative_base()


class Projects(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, autoincrement=False)


def _get_session(connection_url):
    engine = create_engine(connection_url)
    session = Session(engine)
    Base.metadata.create_all(engine)

    return session


class DatabaseWorker():
    _INSTANCE: Self = None

    def __new__(cls) -> Self:
        if cls._INSTANCE:
            return cls._INSTANCE
        else:
            return super().__new__(cls)

    def __init__(self) -> None:
        self._session = _get_session(DB_CONNECTION_URL)

    def add_project(self, id: int):
        try:
            with self._session.begin():
                self._session.add(Projects(id=id))
        except IntegrityError:
            self._session.rollback()

    def add_projetcs(self, ids: List[int]):
        with self._session.begin():
            existed_projects = self._session.query(Projects).filter(
                Projects.id.in_(ids)
            ).all()

            existed_projects = map(lambda prj: prj.id, existed_projects)
            new_projects = filter(lambda id: id in existed_projects, ids)

            self._session.add_all(Projects(id=id) for id in new_projects)
