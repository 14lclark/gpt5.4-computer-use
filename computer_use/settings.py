from logging import getLogger
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

log = getLogger("computer-use-logger")


class LLMSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CLICKS_")
    openai_api_key: str


class FileSystemSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CLICKS_")
    screenshot_output_dir: Path = "/config/"


llm_settings = LLMSettings()
filesystem_settings = FileSystemSettings()
