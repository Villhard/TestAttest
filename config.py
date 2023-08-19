"""Module for reading config from .env file and create config object."""
from dataclasses import dataclass

from environs import Env


@dataclass
class BotConfig:
    """Config for telegram bot."""

    token: str
    admin_ids: list[int]


def load_config(path: str = None) -> BotConfig:
    """Read env and return config."""
    env = Env()
    env.read_env(path)

    return BotConfig(
        token=env("BOT_TOKEN"),
        admin_ids=[int(admin_id) for admin_id in env.list("ADMIN_IDS")],
    )


config = load_config()
