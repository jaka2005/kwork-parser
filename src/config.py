from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """
    Environment settings for the bot
    """

    db_connection_url: str = Field(default=...)
    token: str = Field(default=...)
    category: int = Field(default=...)
    chat_id: int = Field(default=...)
    period: int = Field(default=...)


@lru_cache()
def get_config() -> Config:
    return Config()


MESSAGE_TEXT = """
{title}
Желаемый бюджет: {price} Рублей

{description}
"""

# Time between sending next kwork if there is more than 1
SEND_KWORK_TIMEOUT = 1 / 2

BASE_URL = "https://kwork.ru"
PROJECTS_URL = BASE_URL + "/projects"
KWORK_URL = PROJECTS_URL + "/{id}/view"
NEW_OFFER_URL = BASE_URL + "/new_offer?project={id}"
