from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine.url import make_url
from .config import settings

# Añadir client_encoding a la URL si no está presente
url = make_url(settings.DATABASE_URL)

# Solo agrega el parámetro si no existe
if "client_encoding" not in url.query:
    url = url.set(query={**url.query, "client_encoding": "utf8"})

engine = create_engine(url, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
