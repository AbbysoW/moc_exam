import json
from typing import Any, Dict, Optional

from sqlalchemy import create_engine, select
from sqlalchemy import Integer, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from config import settings


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    role: Mapped[str] = mapped_column(Text, nullable=False)
    login: Mapped[str] = mapped_column(Text, nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)


class DB:
    def __init__(self):
        self._engine = create_engine(
            settings.db.url,
            echo=False,
            json_serializer=lambda obj: json.dumps(
                obj,
                ensure_ascii=False,
            ),
            json_deserializer=json.loads,
        )

        self._sessionmaker = sessionmaker(
            bind=self._engine,
            autoflush=False,
            expire_on_commit=False,
        )

    def init_db(self) -> None:
        """Создаёт таблицу Users, если она ещё не существует."""
        Base.metadata.create_all(
            self._engine,
            tables=[Users.__table__],
        )

    def close(self) -> None:
        self._engine.dispose()

    @staticmethod
    def _record_to_dict(record: Users) -> Dict[str, Any]:
        return {
            column.name: getattr(record, column.name)
            for column in record.__table__.columns
        }

    # CREATE
    def create_user(self, role: str, login: str, password: str, name: str):
        with self._sessionmaker() as session:
            record = Users(
                role=role,
                login=login,
                password=password,
                name=name,
            )

            session.add(record)
            session.flush()

            new_id = record.id
            session.commit()

        return self.read_user_by_id(new_id)

    # READ
    def read_user_by_id(self, record_id: int) -> Optional[Dict[str, Any]]:
        with self._sessionmaker() as session:
            record = session.get(Users, record_id)

            return self._record_to_dict(record) if record else None

    def read_user_by_login(self, login: str) -> Optional[Dict[str, Any]]:
        with self._sessionmaker() as session:
            record = session.scalar(
                select(Users).where(Users.login == login)
            )

            return self._record_to_dict(record) if record else None
