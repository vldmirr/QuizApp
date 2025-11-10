from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "FastAPI Cloud Project"
    environment: str = "development"
    port: int = 8000
    debug: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()