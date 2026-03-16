from logging import getLogger

from pydantic_settings import BaseSettings, SettingsConfigDict

log = getLogger("computer-use-logger")


class LLMSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CLICKS_")
    openai_api_key: str
