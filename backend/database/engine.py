from sqlalchemy import create_engine

from backend.core import settings


engine = create_engine(
    settings.database.database_url,
    echo=settings.app.debug
)