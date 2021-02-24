# -*- coding: utf-8 -*-

from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def initialize_db(engine: Engine) -> None:
    """Initialize DB.

    :param engine: Interface to the DB.
    """
    Base.metadata.create_all(engine)
