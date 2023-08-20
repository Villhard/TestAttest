"""Module for working with user table in database."""
from database.database import User, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(engine)


def check_user_exists(tg_id: int) -> User | None:
    """Check user in DB if exists return user else None."""
    with Session() as session:
        user = session.query(User).filter(User.tg_id == tg_id).first()
        return user


def create_user(tg_id: int, name: str, surname: str) -> None:
    """Create new user in database."""
    with Session() as session:
        user = User(tg_id=tg_id, name=name, surname=surname)
        session.add(user)
        session.commit()
