from sqlite3 import IntegrityError
from typing import List, Optional

from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from typing_extensions import Self

from src.config import get_config

Base = declarative_base()


class Projects(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, autoincrement=False)


def _get_session(connection_url: str) -> Session:
    engine = create_engine(connection_url)
    session = Session(engine)
    Base.metadata.create_all(engine)

    return session


class DatabaseWorker:
    _INSTANCE: Optional[Self] = None

    def __new__(cls) -> Self:
        if cls._INSTANCE:
            return cls._INSTANCE
        else:
            return super().__new__(cls)

    def __init__(self) -> None:
        self._session = _get_session(get_config().db_connection_url)

    def add_project(self, id: int):
        try:
            with self._session.begin():
                self._session.add(Projects(id=id))
        except IntegrityError:
            self._session.rollback()

    def add_projects(self, ids: List[int]) -> List[int]:
        """add new ids and returns ids which not already exists"""

        with self._session.begin():
            existed_projects = (
                self._session.query(Projects).filter(Projects.id.in_(ids)).all()
            )

            existed_projects = tuple(map(lambda prj: prj.id, existed_projects))
            new_projects = list(filter(lambda id: id not in existed_projects, ids))

            self._session.add_all(Projects(id=id) for id in new_projects)

            return new_projects
