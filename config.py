from pydantic import BaseModel, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBConfig(BaseModel):
    dbms: str = "postgresql+psycopg"
    host_url: str
    db: str
    user: str
    password: str

    @computed_field
    @property
    def url(self):
        return f"{self.dbms}://{self.user}:{self.password}@{self.host_url}/{self.db}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        extra="ignore",
    )

    db = DBConfig()

settings = Settings()