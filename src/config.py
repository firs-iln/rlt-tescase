from pydantic_settings import BaseSettings
from pydantic import SecretStr


class DBConfig(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: SecretStr
    DB_NAME: str
    COLLECTION_NAME: str

    class Config:
        env_file = "db.env"
        env_file_encoding = "utf-8"


class BotConfig(BaseSettings):
    TOKEN: SecretStr
    ADMIN_ID: int

    class Config:
        env_file = "bot.env"
        env_file_encoding = "utf-8"


db_config = DBConfig()
bot_config = BotConfig()
