from pathlib import Path

from pydantic import BaseModel, HttpUrl, Field, field_serializer
from pydantic_settings import BaseSettings
from tomli import load
from tomli_w import dump


class DiscordSettings(BaseModel):
    token: str
    invite_link: HttpUrl

    @field_serializer("invite_link")
    def serialize_invite_link(self, value: HttpUrl) -> str:
        return value.__str__()


class BotDatabaseSettings(BaseModel):
    host: HttpUrl
    username: str
    password: str
    database_name: str
    db_prefix: str

    @field_serializer("host")
    def serialize_invite_link(self, value: HttpUrl) -> str:
        return value.__str__()


class BotIntents(BaseModel):
    message_content: bool = Field(default=True)


class BotSettings(BaseSettings):
    prefix: str = Field(default="!")
    bot_name: str = Field(default="Neon Army Core")
    discord_settings: DiscordSettings
    database_settings: BotDatabaseSettings
    intents: BotIntents


def load_config_file(path: Path.name) -> BotSettings:
    with open(path, mode="rb") as file:
        return BotSettings.model_validate(load(file))


def save_config_file(path: Path.name, content: BotSettings):
    with open(path, mode="wb") as file:
        dump(content.model_dump(), file)


async def test_load(path: Path.name):
    config = load_config_file(path)
    print(config)
    print(type(config))


async def test_save(path: Path.name):
    config = BotSettings(
        discord_settings=DiscordSettings(
            token="test",
            invite_link="https://docs.pydantic.dev/latest/errors/validation_errors/#url_syntax_violation",
        ),
        database_settings=BotDatabaseSettings(
            host="http://example.de:8529",
            username="test",
            password="test",
            database_name="test",
            db_prefix="test",
        ),
        intents=BotIntents(),
    )

    print(config.model_dump())
    save_config_file(path, config)


if __name__ == "__main__":
    FILE_PATH = "../../../bot_config_example.toml"
    import asyncio

    asyncio.run(test_save(FILE_PATH))
