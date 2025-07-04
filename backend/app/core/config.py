from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str

    @property
    def adjusted_db_url(self):
        # Añade el parámetro si no está incluido
        if 'client_encoding' not in self.DATABASE_URL:
            if '?' in self.DATABASE_URL:
                return self.DATABASE_URL + '&client_encoding=utf8'
            else:
                return self.DATABASE_URL + '?client_encoding=utf8'
        return self.DATABASE_URL

    class Config:
        env_file = ".env"

settings = Settings()
