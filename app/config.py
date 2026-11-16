from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"
    database_url: str = "sqlite:///./gameon.db"
    kafka_bootstrap_servers: str = "localhost:19092"
    kafka_topic: str = "content.events"
    output_dir: str = "output"
    asset_dir: str = "assets/approved"
    shorts_per_day: int = 5
    tts_model: str = "gpt-4o-mini-tts"
    tts_voice: str = "alloy"
    enable_tts: bool = False
    demo_mode: bool = True
    timezone: str = "Asia/Kolkata"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
