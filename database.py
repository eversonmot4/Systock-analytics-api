import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DB_VIEW_PREFIX = os.getenv("DB_VIEW_PREFIX", "") or ""

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não está definida. Copie .env.example para .env e configure-a.")

# Cria engine do SQLAlchemy (síncrono). Uso somente leitura.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
