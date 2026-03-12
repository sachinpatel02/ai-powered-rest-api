from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gemini_api_key: str
    gemini_model: str = "gemini-2.5-flash"
    max_output_tokens: int = 1024
    temperature: float = 0.3

    class Config:
        env_file = ".env"


settings = Settings()
