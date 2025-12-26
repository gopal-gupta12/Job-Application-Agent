from pydantic import BaseSettings , PostgresDsn , set

class Settings(BaseSettings):
    database_url : PostgresDsn

    class Config:
        env_file  = ".env"

settings = Settings()