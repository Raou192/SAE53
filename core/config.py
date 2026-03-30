from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "TrainBooking API"

    DATABASE_URL: str
    KEYCLOAK_ISSUER: str
    KEYCLOAK_AUDIENCE: str
    KEYCLOAK_INTERNAL_ISSUER: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
