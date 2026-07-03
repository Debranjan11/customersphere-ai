from backend.database.base import Base
from backend.database.engine import engine

import backend.models


def init_db():
    Base.metadata.create_all(bind=engine)