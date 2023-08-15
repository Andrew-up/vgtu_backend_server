from sqlalchemy import create_engine

from definitions import DATABASE_DIR
from repository.abstractRepository import AbstractRepository

ENGINE = create_engine(f"sqlite:///{DATABASE_DIR}", echo=True)
