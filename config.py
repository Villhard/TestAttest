"""
The config module.

Classes:
    BotConfig - configuration of the bot.
    DatabaseConfig - configuration of the database.
    Config - configuration of the application.

Functions:
    load_config:
        Reads the environment variables and returns the configuration.
"""

from dataclasses import dataclass

from environs import Env

from data import lexicon_en, lexicon_ru


@dataclass
class BotConfig:
    """Configuration of the bot."""

    token: str
    admin_ids: list[int]


@dataclass
class DatabaseConfig:
    """Configuration of the database."""

    url: str


@dataclass
class Config:
    """
    Configuration of the application.

    Attributes:
        bot: BotConfig
        database: DatabaseConfig
        pass_score: int - minimum score to pass the test
        language: str - language
    """

    bot: BotConfig
    database: DatabaseConfig
    pass_score: int
    language: str


def load_config(path: str = None) -> Config:
    """Reads the environment variables and returns the configuration."""
    env = Env()
    env.read_env(path)

    return Config(
        bot=BotConfig(
            token=env("BOT_TOKEN"),
            admin_ids=[int(admin_id) for admin_id in env.list("ADMIN_IDS")],
        ),
        database=DatabaseConfig(url=env("URL_DATABASE")),
        pass_score=env.int("PASS_SCORE"),
        language=env("LANGUAGE"),
    )


config = load_config()
lexicon = lexicon_en if config.language == "en" else lexicon_ru
