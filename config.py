"""Модуль читает переменные окружения и возвращает конфигурацию приложения."""
from dataclasses import dataclass

from environs import Env


@dataclass
class BotConfig:
    """Конфигурация бота."""

    token: str
    admin_ids: list[int]


@dataclass
class DatabaseConfig:
    """Конфигурация базы данных."""

    url: str


@dataclass
class Config:
    """
    Конфигурация приложения.

    Содержит в себе конфигурации бота и базы данных.
    """

    bot: BotConfig
    database: DatabaseConfig
    pass_score: int


def load_config(path: str = None) -> BotConfig:
    """Читает переменные окружения и возвращает конфигурацию приложения."""
    env = Env()
    env.read_env(path)

    return Config(
        bot=BotConfig(
            token=env("BOT_TOKEN"),
            admin_ids=[int(admin_id) for admin_id in env.list("ADMIN_IDS")],
        ),
        database=DatabaseConfig(url=env("URL_DATABASE")),
        pass_score=env.int("PASS_SCORE"),
    )


config = load_config()
