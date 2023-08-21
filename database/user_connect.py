"""Модуль работы с базой данных для пользователей."""

from sqlalchemy.orm import sessionmaker

from database.database import User, engine


Session = sessionmaker(engine)


def check_user_exists(tg_id: int) -> User | None:
    """Проверка на существование пользователя в базе данных."""
    with Session() as session:
        user = session.query(User).filter(User.tg_id == tg_id).first()
        return user


def create_user(tg_id: int, name: str, surname: str) -> None:
    """Создание пользователя в базе данных."""
    with Session() as session:
        user = User(tg_id=tg_id, name=name, surname=surname)
        session.add(user)
        session.commit()
